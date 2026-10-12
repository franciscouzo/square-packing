#![feature(portable_simd)]
mod geom;
mod lbfgs;

use geom::*;
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

/// xoshiro256** PRNG.
struct Rng([u64; 4]);

impl Rng {
    fn new(seed: u64) -> Self {
        let mut x = seed.wrapping_add(0x9E3779B97F4A7C15);
        let mut s = [0u64; 4];
        for v in s.iter_mut() {
            x = x.wrapping_add(0x9E3779B97F4A7C15);
            let mut z = x;
            z = (z ^ (z >> 30)).wrapping_mul(0xBF58476D1CE4E5B9);
            z = (z ^ (z >> 27)).wrapping_mul(0x94D049BB133111EB);
            *v = z ^ (z >> 31);
        }
        Rng(s)
    }
    fn next(&mut self) -> u64 {
        let s = &mut self.0;
        let r = s[1].wrapping_mul(5).rotate_left(7).wrapping_mul(9);
        let t = s[1] << 17;
        s[2] ^= s[0];
        s[3] ^= s[1];
        s[1] ^= s[2];
        s[0] ^= s[3];
        s[2] ^= t;
        s[3] = s[3].rotate_left(45);
        r
    }
    fn f(&mut self) -> f64 {
        (self.next() >> 11) as f64 * (1.0 / (1u64 << 53) as f64)
    }
    fn range(&mut self, a: f64, b: f64) -> f64 {
        a + (b - a) * self.f()
    }
    fn below(&mut self, k: usize) -> usize {
        (self.next() % k as u64) as usize
    }
    fn normal(&mut self) -> f64 {
        let u = self.f().max(1e-300);
        let v = self.f();
        (-2.0 * u.ln()).sqrt() * (2.0 * std::f64::consts::PI * v).cos()
    }
}

thread_local! {
    static TAN_HALF: bool = std::env::var("SQ_TANHALF").is_ok();
}

struct Searcher {
    n: usize,
    rng: Rng,
    cs: Vec<(f64, f64)>,
    opt: lbfgs::Lbfgs,
    gbuf: Vec<f64>,
    nbr: Nbr,
}

impl Searcher {
    fn new(n: usize, seed: u64) -> Self {
        Searcher {
            n,
            rng: Rng::new(seed),
            cs: Vec::with_capacity(n),
            opt: lbfgs::Lbfgs::new(3 * n + 1, std::env::var("SQ_M").ok().and_then(|v| v.parse().ok()).unwrap_or(6)),   // measured: 1.5x faster than 10, same polish accuracy
            gbuf: vec![0.0; 3 * n + 1],
            nbr: Nbr::new(),
        }
    }

    /// Minimize s + mu * E for an increasing sequence of mu.
    fn relax(&mut self, z: &mut [f64], mu0: f64, mu1: f64, tol: f64) {
        let n = self.n;
        let mut mu = mu0;
        loop {
            // Optionally work in t = tan(theta/2), where the direction is rational
            // and no sine or cosine is evaluated. Converted per stage, so t cannot
            // wander far from zero and blow up.
            let tanh_param = TAN_HALF.with(|v| *v);
            if tanh_param {
                for i in 0..n {
                    z[3 * i + 2] = (z[3 * i + 2] * 0.5).tan();
                }
            }
            let cs = &mut self.cs;
            let gb = &mut self.gbuf;
            let nb = &mut self.nbr;
            self.opt.minimize(z, 4000, tol, |zz, g| {
                let e = energy_param(zz, n, Some(gb), cs, 0.0, Some(nb), tanh_param);
                for (gi, gbi) in g.iter_mut().zip(gb.iter()) {
                    *gi = mu * gbi;
                }
                g[3 * n] += 1.0;
                zz[3 * n] + mu * e
            });
            if tanh_param {
                for i in 0..n {
                    z[3 * i + 2] = 2.0 * z[3 * i + 2].atan();
                }
                normalize_angles(z, n);
            }
            if std::env::var("SQDEBUG").is_ok() {
                eprintln!("mu={mu:.0e} evals={} s={:.9} e={:.3e}", self.opt.evals, z[3 * n], energy(z, n, None, &mut self.cs));
                self.opt.evals = 0;
            }
            if mu >= mu1 {
                break;
            }
            mu = (mu * 10.0).min(mu1);
        }
        normalize_angles(z, n);
    }

    fn random_init(&mut self, side: f64) -> Vec<f64> {
        let n = self.n;
        let mut z = vec![0.0; 3 * n + 1];
        for i in 0..n {
            z[3 * i] = self.rng.range(0.5, side - 0.5);
            z[3 * i + 1] = self.rng.range(0.5, side - 0.5);
            z[3 * i + 2] = if self.rng.f() < 0.5 { 0.0 } else { self.rng.range(-0.785, 0.785) };
        }
        z[3 * n] = side;
        z
    }

    fn perturb(&mut self, z: &mut [f64]) -> f64 {
        let n = self.n;
        let s = z[3 * n];
        let kind = self.rng.below(10);
        match kind {
            7 => {
                // straighten: snap a few squares to axis-aligned
                let k = 1 + self.rng.below(4.min(n));
                for _ in 0..k {
                    let i = self.rng.below(n);
                    z[3 * i + 2] = 0.0;
                }
                1e2
            }
            8 => {
                // rotate a cluster of squares rigidly about a random point
                let (cx, cy) = (self.rng.range(0.0, s), self.rng.range(0.0, s));
                let r = self.rng.range(1.0, 3.0);
                let a = self.rng.range(-0.4, 0.4);
                let (sa, ca) = a.sin_cos();
                for i in 0..n {
                    let (dx, dy) = (z[3 * i] - cx, z[3 * i + 1] - cy);
                    if dx * dx + dy * dy < r * r {
                        z[3 * i] = cx + dx * ca - dy * sa;
                        z[3 * i + 1] = cy + dx * sa + dy * ca;
                        z[3 * i + 2] += a;
                    }
                }
                1e2
            }
            9 => {
                // slide a cluster of squares
                let (cx, cy) = (self.rng.range(0.0, s), self.rng.range(0.0, s));
                let r = self.rng.range(1.0, 3.0);
                let (ux, uy) = (self.rng.range(-0.6, 0.6), self.rng.range(-0.6, 0.6));
                for i in 0..n {
                    let (dx, dy) = (z[3 * i] - cx, z[3 * i + 1] - cy);
                    if dx * dx + dy * dy < r * r {
                        z[3 * i] += ux;
                        z[3 * i + 1] += uy;
                    }
                }
                1e2
            }
            5 | 6 => {
                // smart reinsertion: move 1-2 squares to the least-overlapping of
                // many sampled spots
                let k = 1 + self.rng.below(2.min(n));
                for _ in 0..k {
                    let i = self.rng.below(n);
                    let mut best = (f64::INFINITY, 0.0, 0.0, 0.0);
                    for _ in 0..64 {
                        let x = self.rng.range(0.5, s - 0.5);
                        let y = self.rng.range(0.5, s - 0.5);
                        let th = if self.rng.f() < 0.5 { 0.0 } else { self.rng.range(-0.785, 0.785) };
                        let e = insertion_cost(z, n, i, x, y, th);
                        if e < best.0 {
                            best = (e, x, y, th);
                        }
                    }
                    z[3 * i] = best.1;
                    z[3 * i + 1] = best.2;
                    z[3 * i + 2] = best.3;
                }
                1e2
            }
            0 | 1 => {
                // relocate a few squares
                let k = 1 + self.rng.below(3.min(n));
                for _ in 0..k {
                    let i = self.rng.below(n);
                    z[3 * i] = self.rng.range(0.5, s - 0.5);
                    z[3 * i + 1] = self.rng.range(0.5, s - 0.5);
                    z[3 * i + 2] = if self.rng.f() < 0.4 { 0.0 } else { self.rng.range(-0.785, 0.785) };
                }
                1e2
            }
            2 => {
                // rotate a few squares
                let k = 1 + self.rng.below(4.min(n));
                for _ in 0..k {
                    let i = self.rng.below(n);
                    z[3 * i + 2] += self.rng.range(-0.5, 0.5);
                }
                1e2
            }
            3 => {
                // global jiggle
                let sig = 0.02 + 0.2 * self.rng.f();
                for i in 0..n {
                    z[3 * i] += sig * self.rng.normal();
                    z[3 * i + 1] += sig * self.rng.normal();
                    z[3 * i + 2] += sig * self.rng.normal();
                }
                1e2
            }
            _ => {
                // squeeze: shrink the container and let squares fight it out
                let f = 1.0 - 0.02 * self.rng.f();
                for i in 0..n {
                    z[3 * i] *= f;
                    z[3 * i + 1] *= f;
                }
                z[3 * n] *= f;
                10.0
            }
        }
    }

    /// Mark the squares that can be carried by the container instead of optimized.
    ///
    /// Not "is it grid aligned": a square wedged between two tilted ones is
    /// aligned but very much in play. What matters is distance through the
    /// contact graph from the tilted squares, so a block of aligned squares
    /// several hops away from any tilt is inert and the rest stays active.
    ///
    /// Inert squares are anchored to a wall rather than to absolute coordinates.
    /// At n=228 eighteen of them sit flush against the right and top walls, and
    /// pinning those in place would pin the side length with them.
    fn classify_inert(z: &[f64], n: usize, tol_deg: f64, hops: usize) -> Vec<Option<Frz>> {
        let s = z[3 * n];
        let tol = tol_deg.to_radians();
        let mut seed: Vec<usize> = Vec::new();
        for i in 0..n {
            let a = z[3 * i + 2].rem_euclid(std::f64::consts::FRAC_PI_2);
            let dev = a.min(std::f64::consts::FRAC_PI_2 - a);
            if dev > tol {
                seed.push(i);
            }
        }
        // contact graph: centres close enough that the two squares can touch
        let mut adj: Vec<Vec<u32>> = vec![Vec::new(); n];
        for i in 0..n {
            for j in (i + 1)..n {
                let dx = z[3 * j] - z[3 * i];
                let dy = z[3 * j + 1] - z[3 * i + 1];
                if dx * dx + dy * dy < 2.1 {
                    adj[i].push(j as u32);
                    adj[j].push(i as u32);
                }
            }
        }
        let mut dist = vec![usize::MAX; n];
        let mut q = std::collections::VecDeque::new();
        for &i in &seed {
            dist[i] = 0;
            q.push_back(i);
        }
        while let Some(i) = q.pop_front() {
            if dist[i] >= hops {
                continue;
            }
            for &j in &adj[i] {
                let j = j as usize;
                if dist[j] == usize::MAX {
                    dist[j] = dist[i] + 1;
                    q.push_back(j);
                }
            }
        }
        (0..n)
            .map(|i| {
                if dist[i] != usize::MAX {
                    return None;
                }
                let (x, y) = (z[3 * i], z[3 * i + 1]);
                let (hix, hiy) = (x > s * 0.5, y > s * 0.5);
                Some(Frz {
                    ox: if hix { s - x } else { x },
                    oy: if hiy { s - y } else { y },
                    hix,
                    hiy,
                    angle: z[3 * i + 2],
                })
            })
            .collect()
    }

    /// Penalty continuation with the inert squares carried by the container.
    fn relax_inert(&mut self, z: &mut [f64], mu0: f64, mu1: f64, tol: f64, frz: &[Option<Frz>]) {
        let n = self.n;
        let mut mu = mu0;
        loop {
            let cs = &mut self.cs;
            let gb = &mut self.gbuf;
            let nb = &mut self.nbr;
            self.opt.minimize(z, 4000, tol, |zz, g| {
                let e = energy_frozen(zz, n, Some(gb), cs, 0.0, Some(nb), false, Some(frz));
                for (gi, gbi) in g.iter_mut().zip(gb.iter()) {
                    *gi = mu * gbi;
                }
                g[3 * n] += 1.0;
                zz[3 * n] + mu * e
            });
            // the frozen squares moved with the side, so put them where they are
            let s = z[3 * n];
            for i in 0..n {
                if let Some(fz) = frz[i] {
                    let (px, py) = fz.pos(s);
                    z[3 * i] = px;
                    z[3 * i + 1] = py;
                    z[3 * i + 2] = fz.angle;
                }
            }
            if mu >= mu1 {
                break;
            }
            mu = (mu * 10.0).min(mu1);
        }
    }

    /// Relax and certify: returns strictly feasible configuration and its side.
    /// Fast, approximate solve used inside the search loop.
    fn solve(&mut self, z: &mut Vec<f64>, mu0: f64) -> f64 {
        self.relax(z, mu0, 1e7, 1e-9);
        make_feasible(z, self.n)
    }

    /// Accurate solve: continue the penalty continuation to a tight tolerance.
    fn polish(&mut self, z: &mut Vec<f64>) -> f64 {
        self.relax(z, 1e6, 1e12, 1e-14);
        make_feasible(z, self.n)
    }

    /// Penalty continuation with some angles pinned. The objective simply ignores
    /// the frozen coordinates (their gradient is zeroed and the energy is evaluated
    /// at the pinned value), so the optimizer repacks everything else around them.
    fn relax_frozen(&mut self, z: &mut [f64], mu0: f64, mu1: f64, tol: f64, frozen: &[bool]) {
        let n = self.n;
        let fixed: Vec<f64> = (0..n).map(|i| z[3 * i + 2]).collect();
        let mut work = z.to_vec();
        let mut mu = mu0;
        loop {
            let cs = &mut self.cs;
            let gb = &mut self.gbuf;
            let nb = &mut self.nbr;
            self.opt.minimize(z, 4000, tol, |zz, g| {
                work.copy_from_slice(zz);
                for i in 0..n {
                    if frozen[i] {
                        work[3 * i + 2] = fixed[i];
                    }
                }
                let e = energy_full(&work, n, Some(gb), cs, 0.0, Some(nb));
                for (gi, gbi) in g.iter_mut().zip(gb.iter()) {
                    *gi = mu * gbi;
                }
                for i in 0..n {
                    if frozen[i] {
                        g[3 * i + 2] = 0.0;
                    }
                }
                g[3 * n] += 1.0;
                zz[3 * n] + mu * e
            });
            for i in 0..n {
                if frozen[i] {
                    z[3 * i + 2] = fixed[i];
                }
            }
            if mu >= mu1 {
                break;
            }
            mu = (mu * 10.0).min(mu1);
        }
    }

    /// Exact-penalty polish. Minimizes s + mu * E_eps with a pseudo-Huber shape
    /// whose effective linear weight 2*mu*eps stays fixed while eps shrinks, so
    /// the contact forces stay O(1) instead of dying with the overlap.
    fn polish_huber(&mut self, z: &mut Vec<f64>) -> f64 {
        let n = self.n;
        let lambda = 60.0;
        for k in 0..7 {
            let eps = 1e-3 * 0.01_f64.powi(k.min(4));
            let mu = lambda / (2.0 * eps);
            let cs = &mut self.cs;
            let gb = &mut self.gbuf;
            let nb = &mut self.nbr;
            self.opt.minimize(z, 4000, 1e-15, |zz, g| {
                let e = energy_full(zz, n, Some(gb), cs, eps, Some(nb));
                for (gi, gbi) in g.iter_mut().zip(gb.iter()) {
                    *gi = mu * gbi;
                }
                g[3 * n] += 1.0;
                zz[3 * n] + mu * e
            });
        }
        normalize_angles(z, n);
        make_feasible(z, n)
    }
}

/// Overlap energy of square i if it were placed at (x, y, th), ignoring walls
/// (candidates are sampled inside the container).
fn insertion_cost(z: &[f64], n: usize, i: usize, x: f64, y: f64, th: f64) -> f64 {
    let (s, c) = th.sin_cos();
    let mut e = 0.0;
    for j in 0..n {
        if j == i {
            continue;
        }
        let dx = z[3 * j] - x;
        let dy = z[3 * j + 1] - y;
        if dx * dx + dy * dy >= 2.0 {
            continue;
        }
        let (sj, cj) = z[3 * j + 2].sin_cos();
        if let Some(hit) = pair_depth(x, y, c, s, z[3 * j], z[3 * j + 1], cj, sj, false) {
            e += hit.depth * hit.depth;
        }
    }
    e
}

/// Pairs of squares that touch (within a hair), plus squares flush against a wall:
/// a simple measure of how tightly a packing is settled.
fn contact_count(z: &[f64], n: usize) -> usize {
    let s = z[3 * n];
    let eps = 1e-9;
    let mut c = 0;
    let cs: Vec<(f64, f64)> = (0..n)
        .map(|i| {
            let (si, ci) = z[3 * i + 2].sin_cos();
            (ci, si)
        })
        .collect();
    for i in 0..n {
        let hh = 0.5 * (cs[i].0.abs() + cs[i].1.abs());
        for (v, lim) in [(z[3 * i], s), (z[3 * i + 1], s)] {
            if (v - hh).abs() < eps || (v + hh - lim).abs() < eps {
                c += 1;
            }
        }
        for j in (i + 1)..n {
            let dx = z[3 * j] - z[3 * i];
            let dy = z[3 * j + 1] - z[3 * i + 1];
            if dx * dx + dy * dy >= 2.1 {
                continue;
            }
            // touching: no overlap now, but overlapping once grown by eps
            if pair_depth(z[3 * i], z[3 * i + 1], cs[i].0, cs[i].1, z[3 * j], z[3 * j + 1], cs[j].0, cs[j].1, false).is_none() {
                let mut zz = [z[3 * i] , z[3 * i + 1]];
                zz[0] += dx.signum() * eps;
                zz[1] += dy.signum() * eps;
                if pair_depth(zz[0], zz[1], cs[i].0, cs[i].1, z[3 * j], z[3 * j + 1], cs[j].0, cs[j].1, false).is_some() {
                    c += 1;
                }
            }
        }
    }
    c
}

/// How many neighbours (and walls) square `i` is touching, within a hair.
fn touch_count(z: &[f64], n: usize, i: usize) -> usize {
    let s = z[3 * n];
    let eps = 1e-9;
    let (si, ci) = z[3 * i + 2].sin_cos();
    let hh = 0.5 * (ci.abs() + si.abs());
    let (x, y) = (z[3 * i], z[3 * i + 1]);
    let mut c = 0;
    for v in [x, y] {
        if (v - hh).abs() < eps || (v + hh - s).abs() < eps {
            c += 1;
        }
    }
    for j in 0..n {
        if j == i {
            continue;
        }
        let dx = z[3 * j] - x;
        let dy = z[3 * j + 1] - y;
        if dx * dx + dy * dy >= 2.1 {
            continue;
        }
        let (sj, cj) = z[3 * j + 2].sin_cos();
        if pair_depth(x, y, ci, si, z[3 * j], z[3 * j + 1], cj, sj, false).is_none()
            && pair_depth(x + dx.signum() * eps, y + dy.signum() * eps, ci, si,
                          z[3 * j], z[3 * j + 1], cj, sj, false).is_some()
        {
            c += 1;
        }
    }
    c
}

struct Shared {
    best_s: f64,
    best_z: Vec<f64>,
    pool: Vec<Vec<f64>>,
}

/// Keep several geometrically distinct near-best states for a stronger
/// downstream optimizer. A slightly worse penalty optimum may LP-refine below
/// the incumbent, so exporting only strict records discards useful basins.
fn offer_pool(pool: &mut Vec<Vec<f64>>, z: &[f64], n: usize, capacity: usize, distance: f64) {
    if capacity == 0 { return; }
    let duplicate = pool.iter().position(|p| {
        (0..n).all(|i| {
            let angle = (p[3*i+2]-z[3*i+2]).rem_euclid(std::f64::consts::FRAC_PI_2);
            (p[3*i]-z[3*i]).abs() < distance
                && (p[3*i+1]-z[3*i+1]).abs() < distance
                && angle.min(std::f64::consts::FRAC_PI_2-angle) < distance
        })
    });
    if let Some(i) = duplicate {
        if z[3*n] < pool[i][3*n] { pool[i] = z.to_vec(); }
    } else if pool.len() < capacity {
        pool.push(z.to_vec());
    } else {
        let worst = (0..pool.len()).max_by(|&i, &j| pool[i][3*n].total_cmp(&pool[j][3*n])).unwrap();
        if z[3*n] < pool[worst][3*n] { pool[worst] = z.to_vec(); }
    }
}

fn load_records() -> std::collections::HashMap<usize, f64> {
    let mut m = std::collections::HashMap::new();
    // Missing file used to fall through silently to ceil(sqrt(n)), which is the
    // trivial grid side -- every run then printed "BEATS RECORD" against a
    // target that was nowhere near the real one. Easy to do by running from the
    // wrong directory, and nothing in the output said so.
    if !std::path::Path::new("records.txt").exists() {
        eprintln!(
            "records.txt not found in {} -- run from the repository root",
            std::env::current_dir().map(|p| p.display().to_string()).unwrap_or_default()
        );
        std::process::exit(2);
    }
    if let Ok(t) = std::fs::read_to_string("records.txt") {
        for line in t.lines() {
            if line.starts_with('#') {
                continue;
            }
            let mut it = line.split_whitespace();
            if let (Some(a), Some(b)) = (it.next(), it.next()) {
                if let (Ok(n), Ok(s)) = (a.parse(), b.parse()) {
                    m.insert(n, s);
                }
            }
        }
    }
    m
}

fn save(path: &str, z: &[f64], n: usize) {
    let mut out = format!("# n = {n}\n# s = {:.15}\n# x y theta(rad)\n", z[3 * n]);
    for i in 0..n {
        out += &format!("{:.17e} {:.17e} {:.17e}\n", z[3 * i], z[3 * i + 1], z[3 * i + 2]);
    }
    std::fs::write(path, out).expect("write result");
    std::fs::write(path.replace(".txt", ".svg"), svg(z, n)).expect("write svg");
}

fn load(path: &str) -> (usize, Vec<f64>) {
    let t = std::fs::read_to_string(path).expect("read file");
    let mut z = Vec::new();
    for line in t.lines() {
        if line.starts_with('#') || line.trim().is_empty() {
            continue;
        }
        for v in line.split_whitespace().take(3) {
            z.push(v.parse::<f64>().expect("number"));
        }
    }
    let n = z.len() / 3;
    z.push(0.0);
    let s = make_feasible(&mut z, n);
    z[3 * n] = s;
    (n, z)
}

fn svg(z: &[f64], n: usize) -> String {
    let s = z[3 * n];
    let sc = 600.0 / s;
    let mut o = format!(
        "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"620\" height=\"650\" viewBox=\"-10 -10 620 650\">\n\
         <rect x=\"0\" y=\"0\" width=\"600\" height=\"600\" fill=\"none\" stroke=\"black\" stroke-width=\"1.5\"/>\n"
    );
    for i in 0..n {
        let (x, y, t) = (z[3 * i], z[3 * i + 1], z[3 * i + 2]);
        let (sn, c) = t.sin_cos();
        let pts: Vec<String> = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]
            .iter()
            .map(|&(a, b)| {
                let px = x + a * c - b * sn;
                let py = y + a * sn + b * c;
                format!("{:.3},{:.3}", px * sc, (s - py) * sc)
            })
            .collect();
        // blue only when the square is exactly axis-aligned; any tilt at all is orange
        let fill = if t != 0.0 { "#f4b183" } else { "#9dc3e6" };
        o += &format!("<polygon points=\"{}\" fill=\"{fill}\" stroke=\"#333\" stroke-width=\"0.8\"/>\n", pts.join(" "));

    }
    o += &format!("<text x=\"0\" y=\"628\" font-family=\"monospace\" font-size=\"16\">n = {n}, s = {s:.9}</text>\n</svg>\n");
    o
}

fn search(n: usize, secs: f64, threads: usize, seed: u64, init: Option<Vec<f64>>, local: bool,
          pool_size: usize, pool_gap: f64, pool_distance: f64) {
    let records = load_records();
    let record = match records.get(&n) {
        Some(r) => *r,
        None => {
            let g = (n as f64).sqrt().ceil();
            eprintln!("warning: no catalogue entry for n={n}; comparing against the trivial grid side {g}");
            g
        }
    };
    let _ = std::fs::create_dir_all("results");
    let path = format!("results/n{n}.txt");
    // start from the previous best result on disk, if any
    // --init with more than n squares: every chain starts from it with random
    // squares removed ("drop" seeding)
    let (prev, drop_from, grow_from) = match init {
        Some(z) if z.len() > 3 * n + 1 => (None, Some(z), None),
        Some(z) if z.len() < 3 * n + 1 => (None, None, Some(z)),
        other => (other, None, None),
    };
    let prev = prev.or_else(|| std::path::Path::new(&path).exists().then(|| load(&path).1));
    let shared = Arc::new(Mutex::new(Shared {
        best_s: prev.as_ref().map(|z| z[3 * n]).unwrap_or(f64::INFINITY),
        best_z: prev.clone().unwrap_or_default(),
        pool: Vec::new(),
    }));
    eprintln!("n={n} record={record:.9} start_best={:.9}", shared.lock().unwrap().best_s);
    let deadline = Instant::now() + Duration::from_secs_f64(secs);
    let mut handles = Vec::new();
    for t in 0..threads {
        let shared = shared.clone();
        let prev = prev.clone();
        let drop_from = drop_from.clone();
        let grow_from = grow_from.clone();
        let path = path.clone();
        handles.push(std::thread::spawn(move || {
            let mut se = Searcher::new(n, seed.wrapping_mul(1000).wrapping_add(t as u64));
            let base = (n as f64).sqrt().ceil() + 0.5;
            let mut restarts = 0u64;
            while Instant::now() < deadline {
                // new chain: from the best-so-far half the time if we have one
                let mut cur = if let Some(big) = &drop_from {
                    let m = (big.len() - 1) / 3;
                    let mut idx: Vec<usize> = (0..m).collect();
                    for k in 0..(m - n) {
                        let r = k + se.rng.below(m - k);
                        idx.swap(k, r);
                    }
                    let mut z: Vec<f64> = Vec::with_capacity(3 * n + 1);
                    for &i in &idx[(m - n)..] {
                        z.extend_from_slice(&big[3 * i..3 * i + 3]);
                    }
                    z.push(big[3 * m]);
                    se.solve(&mut z, 1e3);
                    se.polish(&mut z);
                    z
                } else if let Some(small) = &grow_from {
                    // seed from a packing with fewer squares: insert the missing
                    // ones into the emptiest spots, enlarging the container a little
                    let m = (small.len() - 1) / 3;
                    let mut z = small[..3 * m].to_vec();
                    let s0 = small[3 * m] * (1.0 + 0.02 * se.rng.f());
                    z.resize(3 * n, 0.0);
                    z.push(s0);
                    for k in m..n {
                        let mut best = (f64::INFINITY, 0.0, 0.0, 0.0);
                        for _ in 0..512 {
                            let x = se.rng.range(0.5, s0 - 0.5);
                            let y = se.rng.range(0.5, s0 - 0.5);
                            let th = if se.rng.f() < 0.5 { 0.0 } else { se.rng.range(-0.785, 0.785) };
                            let e = insertion_cost(&z[..3 * k], k, k, x, y, th);
                            if e < best.0 {
                                best = (e, x, y, th);
                            }
                        }
                        z[3 * k] = best.1;
                        z[3 * k + 1] = best.2;
                        z[3 * k + 2] = best.3;
                    }
                    se.solve(&mut z, 1e2);
                    se.polish(&mut z);
                    z
                } else { match (&prev, local || restarts % 2 == 1) {
                    (Some(p), true) => {
                        let b = shared.lock().unwrap().best_z.clone();
                        if b.is_empty() { p.clone() } else { b }
                    }
                    _ => {
                        let mut z = se.random_init(base);
                        se.solve(&mut z, 1.0);
                        se.polish(&mut z);
                        z
                    }
                } };
                restarts += 1;
                let mut cur_s = cur[3 * n];
                let mut temp = 0.01 * se.rng.f();
                let mut since_improve = 0;
                while since_improve < 400 && Instant::now() < deadline {
                    se_count(); let mut trial = cur.clone();
                    let mu0 = se.perturb(&mut trial);
                    let mut s = se.solve(&mut trial, mu0);
                    if s < cur_s + 1e-5 {
                        s = se.polish(&mut trial);
                    }
                    if pool_size > 0 {
                        let mut sh = shared.lock().unwrap();
                        if s <= sh.best_s + pool_gap {
                            offer_pool(&mut sh.pool, &trial, n, pool_size, pool_distance);
                        }
                    }
                    let accept = s < cur_s - 1e-12 || se.rng.f() < (-(s - cur_s) / temp.max(1e-12)).exp();
                    if s < cur_s - 1e-9 {
                        since_improve = 0;
                    } else {
                        since_improve += 1;
                    }
                    if accept {
                        cur = trial;
                        cur_s = s;
                    }
                    temp *= 0.995;
                    let mut sh = shared.lock().unwrap();
                    if cur_s < sh.best_s - 1e-12 {
                        sh.best_s = cur_s;
                        sh.best_z = cur.clone();
                        save(&path, &cur, n);
                        let tag = if cur_s < record - 1e-9 { "  *** BEATS RECORD ***" } else { "" };
                        eprintln!(
                            "[t{t}] n={n} s={cur_s:.10} (record {record:.10}, diff {:+.3e}){tag}",
                            cur_s - record
                        );
                    }
                }
            }
        }));
    }
    for h in handles {
        h.join().unwrap();
    }
    let sh = shared.lock().unwrap();
    if pool_size > 0 {
        std::fs::create_dir_all("pool").unwrap();
        let mut pool = sh.pool.clone();
        pool.sort_by(|a, b| a[3*n].total_cmp(&b[3*n]));
        for (i, z) in pool.iter().enumerate() {
            save(&format!("pool/n{n}_{i}.txt"), z, n);
        }
        eprintln!("n={n} exported {} near-best candidates to pool/", pool.len());
    }
    println!("n={n} best={:.10} record={record:.10} diff={:+.3e} solves={}", sh.best_s, sh.best_s - record, SOLVES.swap(0, std::sync::atomic::Ordering::Relaxed));
}


/// Flatten squares whose tilt is small enough to be worth removing.
///
/// A Rust port of flatten_dust.py, which took two minutes on a 209-square packing
/// with 134 candidates; the inner loop is the same separating-axis test the rest of
/// this file uses. Semantics are unchanged and deliberately conservative: the box
/// the packing arrived in is a hard wall, so the side can never grow, and any square
/// that cannot be freed goes back exactly as it was, so the result is always valid.
fn flatten(path: &str, out: &str, tol_deg: f64) {
    let (n, mut z) = load(path);
    let orig = z.clone();
    let ext = |t: f64| {
        let (s, c) = t.sin_cos();
        0.5 * (c.abs() + s.abs())
    };
    let (mut x0, mut y0) = (f64::INFINITY, f64::INFINITY);
    let (mut x1, mut y1) = (f64::NEG_INFINITY, f64::NEG_INFINITY);
    for i in 0..n {
        let e = ext(z[3 * i + 2]);
        x0 = x0.min(z[3 * i] - e);
        x1 = x1.max(z[3 * i] + e);
        y0 = y0.min(z[3 * i + 1] - e);
        y1 = y1.max(z[3 * i + 1] + e);
    }
    let side0 = (x1 - x0).max(y1 - y0);
    let clear = (side0 * 1e-15).max(1e-16);
    let tol = tol_deg.to_radians();

    let mut free: Vec<usize> = (0..n)
        .filter(|&i| z[3 * i + 2] != 0.0 && z[3 * i + 2].abs() < tol)
        .collect();
    let total = free.len();
    for &i in &free {
        z[3 * i + 2] = 0.0;
    }

    // depth and push-out direction for i against j, or None when disjoint
    let pen = |z: &[f64], i: usize, j: usize| -> Option<(f64, f64, f64)> {
        let (si, ci) = z[3 * i + 2].sin_cos();
        let (sj, cj) = z[3 * j + 2].sin_cos();
        let (dx, dy) = (z[3 * j] - z[3 * i], z[3 * j + 1] - z[3 * i + 1]);
        let mut best: Option<(f64, f64, f64)> = None;
        for (oc, os, tc, ts) in [(ci, si, cj, sj), (cj, sj, ci, si)] {
            for k in 0..2 {
                let (uc, us) = if k == 0 { (oc, os) } else { (-os, oc) };
                let p = dx * uc + dy * us;
                let pc = uc * tc + us * ts;
                let ps = us * tc - uc * ts;
                let o = 0.5 + 0.5 * (pc.abs() + ps.abs()) - p.abs();
                if o <= 0.0 {
                    return None;
                }
                if best.map_or(true, |b| o < b.0) {
                    let sign = if p > 0.0 { -1.0 } else { 1.0 };
                    best = Some((o, uc * sign, us * sign));
                }
            }
        }
        best
    };

    let spread = |z: &mut Vec<f64>, free: &[usize], set: &std::collections::HashSet<usize>| {
        for _ in 0..500 {
            let mut moved = 0.0;
            for &i in free {
                for j in 0..n {
                    if j == i {
                        continue;
                    }
                    let dx = z[3 * j] - z[3 * i];
                    let dy = z[3 * j + 1] - z[3 * i + 1];
                    if dx * dx + dy * dy > 4.0 {
                        continue;
                    }
                    if let Some((d, nx, ny)) = pen(z, i, j) {
                        let step = (d + clear) * if set.contains(&j) { 0.5 } else { 1.0 };
                        z[3 * i] += nx * step;
                        z[3 * i + 1] += ny * step;
                        let e = ext(z[3 * i + 2]);
                        z[3 * i] = z[3 * i].clamp(x0 + e, x1 - e);
                        z[3 * i + 1] = z[3 * i + 1].clamp(y0 + e, y1 - e);
                        moved += step;
                    }
                }
            }
            if moved < 1e-18 {
                break;
            }
        }
    };

    let mut set: std::collections::HashSet<usize> = free.iter().copied().collect();
    spread(&mut z, &free, &set);

    // Give up one square at a time, worst first, and let the rest settle again.
    for _ in 0..(total + 1) {
        let mut worst: Option<(f64, usize)> = None;
        for &i in &free {
            let e = ext(z[3 * i + 2]);
            let out_of_box = z[3 * i] - e < x0 - 1e-12
                || z[3 * i + 1] - e < y0 - 1e-12
                || z[3 * i] + e > x1 + 1e-12
                || z[3 * i + 1] + e > y1 + 1e-12;
            let mut deepest: f64 = if out_of_box { 1.0 } else { 0.0 };
            for j in 0..n {
                if j == i {
                    continue;
                }
                let dx = z[3 * j] - z[3 * i];
                let dy = z[3 * j + 1] - z[3 * i + 1];
                if dx * dx + dy * dy > 4.0 {
                    continue;
                }
                if let Some((d, _, _)) = pen(&z, i, j) {
                    deepest = deepest.max(d);
                }
            }
            if deepest > 0.0 && worst.map_or(true, |w| deepest > w.0) {
                worst = Some((deepest, i));
            }
        }
        match worst {
            None => break,
            Some((_, i)) => {
                z[3 * i] = orig[3 * i];
                z[3 * i + 1] = orig[3 * i + 1];
                z[3 * i + 2] = orig[3 * i + 2];
                free.retain(|&k| k != i);
                set.remove(&i);
                spread(&mut z, &free, &set);
            }
        }
    }

    let side = make_feasible(&mut z, n);
    save(out, &z, n);
    println!(
        "flattened {} of {} candidates; side {:.15} -> {:.15}",
        free.len(),
        total,
        side0,
        side
    );
}

fn verify(path: &str) {
    let t = std::fs::read_to_string(path).expect("read file");
    let mut z = Vec::new();
    for line in t.lines() {
        if line.starts_with('#') || line.trim().is_empty() {
            continue;
        }
        for v in line.split_whitespace().take(3) {
            z.push(v.parse::<f64>().unwrap());
        }
    }
    let n = z.len() / 3;
    z.push(0.0);
    let ov = max_overlap(&z, n);
    let (x0, y0, x1, y1) = bbox(&z, n);
    println!(
        "n={n} max_pair_overlap={ov:.3e} bbox_side={:.12} (x:[{x0:.3e},{x1:.9}] y:[{y0:.3e},{y1:.9}])",
        (x1 - x0).max(y1 - y0)
    );
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let get = |flag: &str, def: &str| -> String {
        args.iter()
            .position(|a| a == flag)
            .and_then(|i| args.get(i + 1).cloned())
            .unwrap_or_else(|| def.to_string())
    };
    let cores = std::thread::available_parallelism().map(|v| v.get()).unwrap_or(1).to_string();
    match args.get(1).map(|s| s.as_str()) {
        Some("search") => {
            let ns: Vec<usize> = args[2].split(',').map(|v| v.parse().unwrap()).collect();
            let secs: f64 = get("--time", "60").parse().unwrap();
            let threads: usize = get("--threads", &cores).parse().unwrap();
            let seed: u64 = get("--seed", "1").parse().unwrap();
            let pool_size: usize = get("--pool", "0").parse().unwrap();
            let pool_gap: f64 = get("--pool-gap", "0.005").parse().unwrap();
            let pool_distance: f64 = get("--pool-distance", "0.005").parse().unwrap();
            assert!(pool_gap.is_finite() && pool_gap >= 0.0);
            assert!(pool_distance.is_finite() && pool_distance > 0.0);
            for n in ns {
                let init = args.iter().position(|a| a == "--init").map(|i| load(&args[i + 1]).1);
                search(n, secs, threads, seed, init, args.iter().any(|a| a == "--local"),
                       pool_size, pool_gap, pool_distance);
            }
        }
        Some("verify") => verify(&args[2]),
        Some("flatten") => {
            let tol: f64 = get("--tol", "10").parse().unwrap();
            let out = get("--out", "");
            flatten(&args[2], if out.is_empty() { &args[2] } else { &out }, tol);
        }
        Some("contacts") => {
            // How tightly a packing is settled: touching pairs plus wall contacts.
            let (n, z) = load(&args[2]);
            println!("{}", contact_count(&z, n));
        }
        Some("bench") => {
            // Fixed work, not fixed time, so two builds can be compared directly.
            let n: usize = args[2].parse().unwrap();
            let (n, z) = load(&format!("records/n{n}.txt"));
            let mut cs = Vec::new();
            let mut g = vec![0.0; 3 * n + 1];
            let evals: usize = get("--evals", "20000").parse().unwrap();
            let mut nbr = Nbr::new();
            let no_list = std::env::var("SQ_NONBR").is_ok(); // A/B against the full scan
            let t0 = Instant::now();
            let mut acc = 0.0;
            for _ in 0..evals {
                let nb = if no_list { None } else { Some(&mut nbr) };
                acc += energy_full(&z, n, Some(&mut g), &mut cs, 0.0, nb);
            }
            let dt = t0.elapsed().as_secs_f64();
            let pairs = (n * (n - 1) / 2) as f64;
            println!(
                "n={n} energy+grad: {:.2} us/call  {:.1} Mpair-tests/s  (acc {acc:.3e})",
                dt / evals as f64 * 1e6,
                pairs * evals as f64 / dt / 1e6
            );
            let solves: usize = get("--solves", "30").parse().unwrap();
            let mut se = Searcher::new(n, 12345);
            let t1 = Instant::now();
            let mut sum = 0.0;
            for _ in 0..solves {
                let mut zz = z.clone();
                let mu0 = se.perturb(&mut zz);
                sum += se.solve(&mut zz, mu0);
            }
            let dt1 = t1.elapsed().as_secs_f64();
            println!(
                "n={n} solve: {:.1} ms each  {:.2} solves/s  (sum {sum:.6})",
                dt1 / solves as f64 * 1e3,
                solves as f64 / dt1
            );
        }
        Some("settle") => {
            // Slide loose squares until they touch. Moves are pure translations
            // toward the lower-left, so the packing stays valid and the bounding
            // box can only shrink: the side length never gets worse.
            let path = &args[2];
            let (n, mut z) = load(path);
            let before = z[3 * n];
            let s = before;
            let feasible = |z: &[f64], i: usize| -> bool {
                let (si, ci) = z[3 * i + 2].sin_cos();
                let hh = 0.5 * (ci.abs() + si.abs());
                let (x, y) = (z[3 * i], z[3 * i + 1]);
                if x - hh < 0.0 || y - hh < 0.0 || x + hh > s || y + hh > s {
                    return false;
                }
                for j in 0..n {
                    if j == i {
                        continue;
                    }
                    let dx = z[3 * j] - x;
                    let dy = z[3 * j + 1] - y;
                    if dx * dx + dy * dy >= 2.0 {
                        continue;
                    }
                    let (sj, cj) = z[3 * j + 2].sin_cos();
                    if pair_depth(x, y, ci, si, z[3 * j], z[3 * j + 1], cj, sj, false).is_some() {
                        return false;
                    }
                }
                true
            };
            // Each square is pushed toward the wall it is already nearest, so the
            // border rows end up flush with the container instead of all the slack
            // collecting on two sides.
            let outward = args.iter().any(|a| a == "--outward");
            // Which way each square is pushed. Different schedules leave the slack in
            // different places, so all of them are tried and the tightest kept.
            let schedule: usize = get("--schedule", "1").parse().unwrap();
            // Straighten whatever can be straightened for free. Rotating a square
            // to axis-aligned about its own centre shrinks its axis-aligned extent,
            // so it can never push the container outward; a snap that would overlap
            // a neighbour is simply rejected. Interleaved with sliding, because each
            // makes room for the other.
            let snap_tol = get("--snap", "1.0").parse::<f64>().unwrap().to_radians();
            let mut snapped = 0;
            let mut total = 0.0f64;
            for sweep in 0..200 {
                for i in 0..n {
                    let a = z[3 * i + 2];
                    if a == 0.0 || a.abs() >= snap_tol {
                        continue;
                    }
                    let (x0, y0) = (z[3 * i], z[3 * i + 1]);
                    z[3 * i + 2] = 0.0;
                    if feasible(&z, i) {
                        snapped += 1;
                        continue;
                    }
                    // A square wedged in a row between two exact contacts cannot
                    // straighten alone: whichever way it turns it meets a neighbour.
                    // Try flattening it together with the near-aligned squares it
                    // meets, which is what a whole row of them needs.
                    {
                        let mut group: Vec<usize> = Vec::new();
                        let (si, ci) = (0.0_f64, 1.0_f64); // angle 0 for square i
                        let hh = 0.5 * (ci.abs() + si.abs());
                        for j in 0..n {
                            if j == i {
                                continue;
                            }
                            let dx = z[3 * j] - x0;
                            let dy = z[3 * j + 1] - y0;
                            if dx * dx + dy * dy >= 2.0 {
                                continue;
                            }
                            let (sj, cj) = z[3 * j + 2].sin_cos();
                            if pair_depth(x0, y0, ci, si, z[3 * j], z[3 * j + 1], cj, sj, false).is_some()
                                && z[3 * j + 2] != 0.0
                                && z[3 * j + 2].abs() < snap_tol
                            {
                                group.push(j);
                            }
                        }
                        let _ = hh;
                        if !group.is_empty() && group.len() <= 6 {
                            let saved: Vec<f64> = group.iter().map(|&j| z[3 * j + 2]).collect();
                            for &j in &group {
                                z[3 * j + 2] = 0.0;
                            }
                            let ok = feasible(&z, i) && group.iter().all(|&j| feasible(&z, j));
                            if ok {
                                snapped += 1 + group.len();
                                continue;
                            }
                            for (k, &j) in group.iter().enumerate() {
                                z[3 * j + 2] = saved[k];
                            }
                        }
                    }

                    // A square is often tilted only so a diagonal neighbour's corner
                    // can pass; straightening it then needs a nudge of a thousandth.
                    let mut fixed = false;
                    // First try sitting exactly flush against a wall (or in a corner):
                    // where the square must land precisely for a diagonal neighbour to
                    // just touch, no search over displacements can land on it.
                    let hh = 0.5_f64;
                    for (cx, cy) in [
                        (hh, y0), (s - hh, y0), (x0, hh), (x0, s - hh),
                        (hh, hh), (s - hh, hh), (hh, s - hh), (s - hh, s - hh),
                    ] {
                        z[3 * i] = cx;
                        z[3 * i + 1] = cy;
                        if feasible(&z, i) {
                            fixed = true;
                            break;
                        }
                    }
                    if fixed {
                        snapped += 1;
                        continue;
                    }
                    z[3 * i] = x0;
                    z[3 * i + 1] = y0;
                    'nudge: for (dx, dy) in [
                        (-1.0, 0.0), (1.0, 0.0), (0.0, -1.0), (0.0, 1.0),
                        (-0.707, -0.707), (0.707, -0.707), (-0.707, 0.707), (0.707, 0.707),
                    ] {
                        // A ladder from 1e-13 up to a fifth. The bottom matters as
                        // much as the top: a square wedged between exact contacts is
                        // off axis by a billionth of a degree and needs a nudge of
                        // about 1e-11 to come free, while one tilted to let a corner
                        // pass needs a thousandth.
                        for k in 0..70 {
                            let d = 1e-13 * 1.6_f64.powi(k);
                            if d > 0.2 {
                                break;
                            }
                            z[3 * i] = x0 + dx * d;
                            z[3 * i + 1] = y0 + dy * d;
                            if feasible(&z, i) {
                                fixed = true;
                                break 'nudge;
                            }
                        }
                    }
                    // Last resort: push the square and whatever it runs into, all by
                    // the same step. A square wedged between two aligned neighbours
                    // only comes free if the run it sits in shifts with it.
                    if !fixed {
                        let saved_all = z.to_vec();
                        let overlaps = |z: &[f64], p: usize, q: usize| -> bool {
                            let (sp, cp) = z[3 * p + 2].sin_cos();
                            let (sq, cq) = z[3 * q + 2].sin_cos();
                            pair_depth(z[3 * p], z[3 * p + 1], cp, sp, z[3 * q], z[3 * q + 1], cq, sq, false).is_some()
                        };
                        'chain: for (dx, dy) in [
                            (-1.0, 0.0), (1.0, 0.0), (0.0, -1.0), (0.0, 1.0),
                        ] {
                            for k in 0..45 {
                                let d = 1e-13 * 2.0_f64.powi(k);
                                if d > 1e-3 {
                                    break;
                                }
                                z.copy_from_slice(&saved_all);
                                z[3 * i + 2] = 0.0;
                                z[3 * i] = x0 + dx * d;
                                z[3 * i + 1] = y0 + dy * d;
                                let mut chain = vec![i];
                                let mut settled = false;
                                for _ in 0..8 {
                                    let mut hit = None;
                                    'find: for &m in &chain {
                                        for j in 0..n {
                                            if !chain.contains(&j) && overlaps(&z, m, j) {
                                                hit = Some(j);
                                                break 'find;
                                            }
                                        }
                                    }
                                    match hit {
                                        None => {
                                            settled = chain.iter().all(|&m| feasible(&z, m));
                                            break;
                                        }
                                        Some(j) => {
                                            z[3 * j] += dx * d;
                                            z[3 * j + 1] += dy * d;
                                            chain.push(j);
                                        }
                                    }
                                }
                                if settled {
                                    fixed = true;
                                    break 'chain;
                                }
                            }
                        }
                        if !fixed {
                            z.copy_from_slice(&saved_all);
                        }
                    }
                    if fixed {
                        snapped += 1;
                    } else {
                        z[3 * i] = x0;
                        z[3 * i + 1] = y0;
                        z[3 * i + 2] = a;
                    }
                }
                let _ = sweep;
                let mut moved = 0.0f64;
                for i in 0..n {
                    let (x, y) = (z[3 * i], z[3 * i + 1]);
                    let (sx, sy) = (
                        if x > s / 2.0 { 1.0 } else { -1.0 },
                        if y > s / 2.0 { 1.0 } else { -1.0 },
                    );
                    let (dxw, dyw) = (x.min(s - x), y.min(s - y));
                    let dirs = if !outward {
                        [(-1.0, 0.0), (0.0, -1.0)]
                    } else {
                        match schedule {
                            // press to the nearest wall, then run along it leftward/downward
                            1 => {
                                if dyw <= dxw {
                                    [(0.0, sy), (-1.0, 0.0)]
                                } else {
                                    [(sx, 0.0), (0.0, -1.0)]
                                }
                            }
                            // press to the nearest wall, then run toward the nearest corner
                            2 => {
                                if dyw <= dxw {
                                    [(0.0, sy), (sx, 0.0)]
                                } else {
                                    [(sx, 0.0), (0.0, sy)]
                                }
                            }
                            // outward in both axes
                            3 => [(sx, 0.0), (0.0, sy)],
                            // toward the upper right
                            4 => [(1.0, 0.0), (0.0, 1.0)],
                            // Gravity along each square's OWN frame. For a tilted band
                            // this slides every square along the band in one direction,
                            // so the slivers between them merge into one gap at the end
                            // instead of staying scattered. Monotone, so it settles.
                            7 => {
                                let (sa, ca) = z[3 * i + 2].sin_cos();
                                [(ca, sa), (-sa, ca)]
                            }
                            8 => {
                                let (sa, ca) = z[3 * i + 2].sin_cos();
                                [(-ca, -sa), (sa, -ca)]
                            }
                            9 => {
                                let (sa, ca) = z[3 * i + 2].sin_cos();
                                [(ca, sa), (sa, -ca)]
                            }
                            10 => {
                                let (sa, ca) = z[3 * i + 2].sin_cos();
                                [(-ca, -sa), (-sa, ca)]
                            }
                            // press to the nearest wall, then run along it rightward/upward
                            _ => {
                                if dyw <= dxw {
                                    [(0.0, sy), (1.0, 0.0)]
                                } else {
                                    [(sx, 0.0), (0.0, 1.0)]
                                }
                            }
                        }
                    };
                    // the two primary directions, plus their diagonal: a square can
                    // sometimes drop into a hole that neither axis move reaches
                    let diag = {
                        let (ax, ay) = dirs[0];
                        let (bx, by) = dirs[1];
                        let (vx, vy): (f64, f64) = (ax + bx, ay + by);
                        let len: f64 = (vx * vx + vy * vy).sqrt().max(1e-300);
                        (vx / len, vy / len)
                    };
                    // Schedule 6 ignores the wall preference and simply takes the
                    // longest slide available in any of eight directions, which is
                    // what closes a gap sitting in the middle of a row: the fixed
                    // schedules can push two neighbours apart instead of together.
                    // Global axes and diagonals, plus the square's OWN frame. A
                    // square inside a tilted band has to slide along the band to
                    // nestle against its neighbours; axis-aligned moves can only
                    // approach such a contact at a glancing angle and stop short.
                    let (sa, ca) = z[3 * i + 2].sin_cos();
                    let greedy = [
                        (-1.0, 0.0), (1.0, 0.0), (0.0, -1.0), (0.0, 1.0),
                        (-0.70710678, -0.70710678), (0.70710678, -0.70710678),
                        (-0.70710678, 0.70710678), (0.70710678, 0.70710678),
                        (ca, sa), (-ca, -sa), (-sa, ca), (sa, -ca),
                        ((ca - sa) * 0.70710678, (sa + ca) * 0.70710678),
                        ((sa - ca) * 0.70710678, (-sa - ca) * 0.70710678),
                        ((ca + sa) * 0.70710678, (sa - ca) * 0.70710678),
                        ((-ca - sa) * 0.70710678, (ca - sa) * 0.70710678),
                    ];
                    if schedule == 6 {
                        // Slide to whichever contact leaves this square touching the
                        // most neighbours, not to whichever slide is longest: taking
                        // the longest one makes squares wander from gap to gap and
                        // never settle. Contacts only ever go up, so this converges.
                        let (x0, y0) = (z[3 * i], z[3 * i + 1]);
                        let here = touch_count(&z, n, i);
                        let mut best = (here, 0.0f64, (0.0f64, 0.0f64));
                        for (dx, dy) in greedy {
                            let (mut lo, mut hi) = (0.0f64, 2.0f64);
                            for _ in 0..44 {
                                let mid = 0.5 * (lo + hi);
                                z[3 * i] = x0 + dx * mid;
                                z[3 * i + 1] = y0 + dy * mid;
                                if feasible(&z, i) { lo = mid } else { hi = mid }
                            }
                            z[3 * i] = x0 + dx * lo;
                            z[3 * i + 1] = y0 + dy * lo;
                            let c = touch_count(&z, n, i);
                            if lo > 1e-12 && (c > best.0 || (c == best.0 && best.2 != (0.0, 0.0) && lo < best.1)) {
                                best = (c, lo, (dx, dy));
                            }
                            z[3 * i] = x0;
                            z[3 * i + 1] = y0;
                        }
                        if best.2 != (0.0, 0.0) {
                            z[3 * i] = x0 + best.2.0 * best.1;
                            z[3 * i + 1] = y0 + best.2.1 * best.1;
                            moved += best.1;
                        }
                        continue;
                    }
                    for (dx, dy) in [dirs[0], dirs[1], diag, dirs[0], dirs[1]] {
                        let (x0, y0) = (z[3 * i], z[3 * i + 1]);
                        let (mut lo, mut hi) = (0.0f64, 2.0f64);
                        // largest slide that stays valid, by bisection: 26 steps
                        // resolves 3e-8, which is far below anything visible and
                        // well inside the tolerance the later flatten pass needs
                        for _ in 0..44 {
                            let mid = 0.5 * (lo + hi);
                            z[3 * i] = x0 + dx * mid;
                            z[3 * i + 1] = y0 + dy * mid;
                            if feasible(&z, i) { lo = mid } else { hi = mid }
                        }
                        z[3 * i] = x0 + dx * lo;
                        z[3 * i + 1] = y0 + dy * lo;
                        moved += lo;
                    }
                }
                total += moved;
                if moved < 1e-12 {
                    break;
                }
            }
            let after = make_feasible(&mut z, n);
            let contacts = contact_count(&z, n);
            println!("n={n} schedule={schedule} straightened={snapped} slid={total:.4} contacts={contacts}  s: {before:.12} -> {after:.12} ({:+.3e})", after - before);
            let out = args.iter().position(|a| a == "--out").map(|i| args[i + 1].clone());
            match out {
                Some(o) => {
                    save(&o, &z, n);
                    println!("  written to {o}");
                }
                None => println!("  (dry run; pass --out FILE to write)"),
            }
        }
        Some("straighten") => {
            // Snap angles within TOL degrees of axis-aligned to exactly 0, then
            // repack everything else around them. Cosmetic in intent, but it must
            // still pay for itself: the result is kept only if it stays valid.
            let path = &args[2];
            let tol_deg: f64 = get("--tol", "0.2").parse().unwrap();
            let (n, mut z) = load(path);
            let before = z[3 * n];
            let mut frozen = vec![false; n];
            let mut snapped = 0;
            let border_only = args.iter().any(|a| a == "--border");
            // Pin one specific square and leave every other angle free. Pinning
            // the whole already-aligned set alongside it is an extra constraint
            // that can hide a straightening that would otherwise be free.
            let only: Option<usize> = args.iter().position(|a| a == "--only")
                .map(|i| args[i + 1].parse().unwrap());
            let s0 = z[3 * n];
            if let Some(k) = only {
                z[3 * k + 2] = 0.0;
                frozen[k] = true;
                snapped = 1;
            }
            for i in 0..n {
                if only.is_some() {
                    break;
                }
                if border_only {
                    // only squares touching a wall of the container
                    let (si, ci) = z[3 * i + 2].sin_cos();
                    let hh = 0.5 * (ci.abs() + si.abs());
                    let (x, y) = (z[3 * i], z[3 * i + 1]);
                    let gap = (x - hh).min(y - hh).min(s0 - x - hh).min(s0 - y - hh);
                    if gap > 1e-6 {
                        continue;
                    }
                }
                let a = z[3 * i + 2];
                let d = a.to_degrees();
                let q = (d / 90.0).round() * 90.0;
                if (d - q).abs() < tol_deg {
                    z[3 * i + 2] = 0.0; // squares have 90-degree symmetry
                    frozen[i] = true;
                    if (d - q).abs() > 0.0 {
                        snapped += 1;
                    }
                }
            }
            let mut se = Searcher::new(n, 7);
            if args.iter().any(|a| a == "--greedy") {
                // One square at a time, keeping only the ones that are free.
                // Snapping all of them together prices the whole batch: a single
                // square that cannot straighten without opening the container
                // hides every other square that could have.
                let base = before;
                let mut keep = vec![false; n];
                for i in 0..n {
                    if z[3 * i + 2] == 0.0 {
                        keep[i] = true; // already aligned; hold it there
                    }
                }
                let (_, orig) = load(path);
                let mut best = orig.clone();
                let mut cands: Vec<(f64, usize)> = (0..n)
                    .filter(|&i| frozen[i] && orig[3 * i + 2] != 0.0)
                    .map(|i| {
                        let d = orig[3 * i + 2].to_degrees();
                        ((d - (d / 90.0).round() * 90.0).abs(), i)
                    })
                    .collect();
                cands.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
                let mut taken = 0;
                for (dev, i) in cands {
                    let mut trial = best.clone();
                    trial[3 * i + 2] = 0.0;
                    let mut k = keep.clone();
                    k[i] = true;
                    se.relax_frozen(&mut trial, 1e2, 1e12, 1e-14, &k);
                    let s = make_feasible(&mut trial, n);
                    if s <= base && max_overlap(&trial, n) == 0.0 {
                        best = trial;
                        keep = k;
                        taken += 1;
                        println!("  square {i} (dev {dev:.2e} deg): straightened free, s={s:.12}");
                    } else {
                        println!("  square {i} (dev {dev:.2e} deg): would cost {:+.3e}, skipped", s - base);
                    }
                }
                z = best;
                println!("n={n} greedy: {taken} straightened at no cost to the side");
            } else if let Some(hops) = args.iter().position(|a| a == "--hop") {
                // Basin hopping with the chosen angles pinned at zero throughout.
                // A local relax only asks whether the current arrangement can be
                // straightened; this asks whether some other arrangement can,
                // which is a different question and the one worth asking.
                let rounds: usize = args[hops + 1].parse().unwrap();
                se.relax_frozen(&mut z, 1e2, 1e12, 1e-14, &frozen);
                let mut best = z.clone();
                let mut best_s = make_feasible(&mut best, n);
                println!("  start {best_s:.12} (baseline {before:.12})");
                for r in 0..rounds {
                    let mut trial = best.clone();
                    // shake positions and the free angles; pinned ones stay at 0
                    let sig = 0.01 + 0.08 * se.rng.f();
                    for i in 0..n {
                        trial[3 * i] += sig * se.rng.normal();
                        trial[3 * i + 1] += sig * se.rng.normal();
                        if !frozen[i] {
                            trial[3 * i + 2] += sig * se.rng.normal();
                        }
                    }
                    se.relax_frozen(&mut trial, 1e2, 1e12, 1e-14, &frozen);
                    let s = make_feasible(&mut trial, n);
                    if s < best_s && max_overlap(&trial, n) == 0.0 {
                        best_s = s;
                        best = trial;
                        println!("  round {r}: {best_s:.12} ({:+.3e} vs baseline)", best_s - before);
                    }
                }
                z = best;
                println!("n={n} hop: best with angles pinned = {best_s:.12} ({:+.3e} vs baseline)", best_s - before);
            } else {
                se.relax_frozen(&mut z, 1e2, 1e12, 1e-14, &frozen);
            }
            let after = make_feasible(&mut z, n);
            println!(
                "n={n} pinned={} of which moved={snapped}  s: {before:.12} -> {after:.12} ({:+.3e})",
                frozen.iter().filter(|v| **v).count(),
                after - before
            );
            let out = args.iter().position(|a| a == "--out").map(|i| args[i + 1].clone());
            match out {
                Some(o) => {
                    save(&o, &z, n);
                    println!("  written to {o}");
                }
                None => println!("  (dry run; pass --out FILE to write)"),
            }
        }
        Some("refine") => {
            // Freeze the inert squares and re-run the continuation on the rest.
            let (n, mut z) = load(&args[2]);
            let tol: f64 = get("--tol", "1.0").parse().unwrap();
            let hops: usize = get("--hops", "2").parse().unwrap();
            let before = z[3 * n];
            let frz = Searcher::classify_inert(&z, n, tol, hops);
            let frozen = frz.iter().filter(|f| f.is_some()).count();
            let mut se = Searcher::new(n, 1);
            let mut w = z.clone();
            se.relax_inert(&mut w, 1e2, 1e12, 1e-14, &frz);
            let after = make_feasible(&mut w, n);
            let ov = max_overlap(&w, n);
            println!(
                "n={n} frozen={frozen}/{n} (tol={tol} deg, hops={hops})  before={before:.12} after={after:.12} change={:+.3e} overlap={ov:.2e}",
                after - before
            );
            // A refinement that grows the side or leaves an overlap is no
            // refinement; the record file only moves on a strict improvement.
            if after < before && ov == 0.0 {
                z = w;
                save(&args[2], &z, n);
                println!("  (improved; file updated)");
            }
        }
        Some("polish") => {
            let (n, mut z) = load(&args[2]);
            let before = z[3 * n];
            let mut se = Searcher::new(n, 1);
            let after = se.polish_huber(&mut z);
            println!("n={n} before={before:.12} after={after:.12} change={:+.3e}", after - before);
            if after < before {
                save(&args[2], &z, n);
                println!("  (improved; file updated)");
            }
        }
        Some("svg") => {
            let (n, z) = load(&args[2]);
            std::fs::write(args[2].replace(".txt", ".svg"), svg(&z, n)).unwrap();
        }
        _ => {
            eprintln!("usage: sqpack search N[,N...] [--time SECS] [--threads T] [--seed S] [--init FILE] [--local]\n       [--pool K] [--pool-gap SIDE] [--pool-distance DIST]\n       sqpack verify FILE\n       sqpack refine FILE [--tol DEG] [--hops H]\n       sqpack svg FILE");
        }
    }
}

static SOLVES: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
fn se_count() {
    SOLVES.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
}

#[cfg(test)]
mod pool_tests {
    use super::*;

    #[test]
    fn pool_replaces_only_with_better_diverse_states() {
        let mut pool = Vec::new();
        offer_pool(&mut pool, &[0.5, 0.5, 0., 2.], 1, 2, 0.01);
        offer_pool(&mut pool, &[0.5001, 0.5, std::f64::consts::FRAC_PI_2, 1.9], 1, 2, 0.01);
        assert_eq!(pool.len(), 1); // same square pose despite 90-degree rotation
        assert_eq!(pool[0][3], 1.9);
        offer_pool(&mut pool, &[0.5002, 0.5, 0., 2.2], 1, 2, 0.01);
        assert_eq!(pool[0][3], 1.9); // worse duplicate must not displace it
        offer_pool(&mut pool, &[0.6, 0.5, 0., 2.1], 1, 2, 0.01);
        offer_pool(&mut pool, &[0.7, 0.5, 0., 1.8], 1, 2, 0.01);
        assert_eq!(pool.len(), 2);
        assert!(pool.iter().all(|p| p[3] <= 1.9));
    }

    #[test]
    fn zero_capacity_does_not_save_candidates() {
        let mut pool = Vec::new();
        offer_pool(&mut pool, &[0.5, 0.5, 0., 2.], 1, 0, 0.01);
        assert!(pool.is_empty());
    }
}
