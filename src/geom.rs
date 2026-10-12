//! Geometry of unit squares: penetration depth via the separating axis theorem,
//! the penalty energy and its analytic gradient.
//!
//! Parameter layout: z = [x0, y0, t0, x1, y1, t1, ..., s], where (x, y) is a
//! square's center, t its rotation angle, and s the container side. The
//! container is [0, s] x [0, s].

pub const HALF_PI: f64 = std::f64::consts::FRAC_PI_2;

/// Half-extent of a unit square rotated by psi, projected on an axis.
#[inline(always)]
fn h_cs(c: f64, s: f64) -> f64 {
    0.5 * (c.abs() + s.abs())
}

/// Derivative of h with respect to psi.
#[inline(always)]
fn dh_cs(c: f64, s: f64) -> f64 {
    0.5 * (-sgn(c) * s + sgn(s) * c)
}

#[inline(always)]
fn sgn(v: f64) -> f64 {
    if v >= 0.0 { 1.0 } else { -1.0 }
}

/// Result of a pair overlap test: depth and partial derivatives of the depth
/// with respect to (ax, ay, at, bx, by, bt).
pub struct PairHit {
    pub depth: f64,
    pub grad: [f64; 6],
}

/// Penetration depth of squares A and B (minimum overlap over the 4 SAT axes).
/// Returns None if they do not overlap. `ac`/`as_` are cos/sin of A's angle.
#[inline(always)]
pub fn pair_depth(
    ax: f64, ay: f64, ac: f64, as_: f64,
    bx: f64, by: f64, bc: f64, bs: f64,
    want_grad: bool,
) -> Option<PairHit> {
    let dx = bx - ax;
    let dy = by - ay;
    let mut best = f64::INFINITY;
    // (owner_is_a, ucos, usin, psi_cos, psi_sin, p)
    let mut arg = (true, 0.0, 0.0, 0.0, 0.0, 0.0);
    for owner_a in [true, false] {
        let (oc, os, tc, ts) = if owner_a { (ac, as_, bc, bs) } else { (bc, bs, ac, as_) };
        for k in 0..2 {
            let (uc, us) = if k == 0 { (oc, os) } else { (-os, oc) };
            let p = dx * uc + dy * us;
            // psi = alpha - theta_other
            let pc = uc * tc + us * ts;
            let ps = us * tc - uc * ts;
            let o = 0.5 + h_cs(pc, ps) - p.abs();
            if o <= 0.0 {
                return None;
            }
            if o < best {
                best = o;
                arg = (owner_a, uc, us, pc, ps, p);
            }
        }
    }
    let mut grad = [0.0; 6];
    if want_grad {
        let (owner_a, uc, us, pc, ps, p) = arg;
        let sg = sgn(p);
        grad[0] = sg * uc;
        grad[1] = sg * us;
        grad[3] = -sg * uc;
        grad[4] = -sg * us;
        let hp = dh_cs(pc, ps);
        // d . u_perp, u_perp = (-sin a, cos a)
        let dperp = -dx * us + dy * uc;
        let own = hp - sg * dperp;
        if owner_a {
            grad[2] = own;
            grad[5] = -hp;
        } else {
            grad[5] = own;
            grad[2] = -hp;
        }
    }
    Some(PairHit { depth: best, grad })
}

/// Penalty energy E(z) = sum over pairs depth^2 + sum of squared wall violations.
/// Writes dE/dz into `g` (same length as z) if provided.
/// Squared penalty (`eps = 0`) or pseudo-Huber penalty (`eps > 0`).
///
/// With eps > 0 a violation d contributes 2*eps*(sqrt(d^2 + eps^2) - eps), which is
/// smooth at 0 but grows *linearly* for d >> eps. A squared penalty's gradient dies
/// as the overlap closes, so the last nanometre of convergence costs unbounded mu;
/// a near-linear one keeps a finite slope and reaches the constrained optimum at
/// finite weight. (Penalty shape argued in github.com/jlevy/squares sqsearch.)
#[inline(always)]
fn shape(d: f64, eps: f64) -> (f64, f64) {
    if eps <= 0.0 {
        (d * d, 2.0 * d)
    } else {
        let r = (d * d + eps * eps).sqrt();
        (2.0 * eps * (r - eps), 2.0 * eps * d / r)
    }
}

pub fn energy(z: &[f64], n: usize, g: Option<&mut [f64]>, cs: &mut Vec<(f64, f64)>) -> f64 {
    energy_full(z, n, g, cs, 0.0, None)
}

/// With `nbr` the pair loop visits only listed neighbours; without it every pair
/// is scanned. The two agree exactly -- the list is built at a radius beyond which
/// squares cannot touch -- so the slow path stays as a check on the fast one.
/// Store the rotation as the tangent of the half angle instead of the angle.
///
/// The geometry never needs the angle itself, only the direction (cos, sin), and
/// that direction is a rational function of t = tan(theta/2): no sine, no cosine,
/// just a divide. (The trick in <https://iquilezles.org/articles/noacos/>: keep
/// vectors, not angles.) The chain rule back to the angle is dtheta/dt = 2/(1+t^2).
#[inline(always)]
pub fn dir_from_t(t: f64) -> (f64, f64) {
    let tt = t * t;
    let d = 1.0 / (1.0 + tt);
    ((1.0 - tt) * d, 2.0 * t * d)
}

pub fn energy_full(
    z: &[f64],
    n: usize,
    g: Option<&mut [f64]>,
    cs: &mut Vec<(f64, f64)>,
    eps: f64,
    nbr: Option<&mut Nbr>,
) -> f64 {
    energy_param(z, n, g, cs, eps, nbr, false)
}

/// How a frozen square is tied to the container.
///
/// Freezing at absolute coordinates would pin the side length: any square flush
/// against the right or top wall sticks out the moment `s` shrinks, and shrinking
/// `s` is the whole objective. So a frozen square stores an offset from a wall and
/// rides that wall inward, which also means its position contributes to dE/ds.
#[derive(Clone, Copy)]
pub struct Frz {
    pub ox: f64,
    pub oy: f64,
    pub hix: bool, // x = s - ox when true, else x = ox
    pub hiy: bool,
    pub angle: f64,
}

impl Frz {
    #[inline]
    pub fn pos(&self, s: f64) -> (f64, f64) {
        (if self.hix { s - self.ox } else { self.ox },
         if self.hiy { s - self.oy } else { self.oy })
    }
}

pub fn energy_param(
    z: &[f64],
    n: usize,
    g: Option<&mut [f64]>,
    cs: &mut Vec<(f64, f64)>,
    eps: f64,
    nbr: Option<&mut Nbr>,
    tan_half: bool,
) -> f64 {
    energy_frozen(z, n, g, cs, eps, nbr, tan_half, None)
}

/// With `frz`, squares marked frozen are not free variables: their position comes
/// from the container side and their stored wall offsets, and their gradient flows
/// into dE/ds instead of into their own coordinates.
pub fn energy_frozen(
    z: &[f64],
    n: usize,
    mut g: Option<&mut [f64]>,
    cs: &mut Vec<(f64, f64)>,
    eps: f64,
    nbr: Option<&mut Nbr>,
    tan_half: bool,
    frz: Option<&[Option<Frz>]>,
) -> f64 {
    let s = z[3 * n];
    let mut e = 0.0;
    if let Some(g) = g.as_deref_mut() {
        g.iter_mut().for_each(|v| *v = 0.0);
    }
    // Positions actually used: a frozen square's comes from the side length. With
    // no frozen set this stays empty and the plain z layout is read directly, so
    // the search path allocates nothing.
    let mut zeff: Vec<f64> = Vec::new();
    if frz.is_some() {
        zeff.extend_from_slice(z);
        for i in 0..n {
            if let Some(fz) = frz.and_then(|f| f[i]) {
                let (px, py) = fz.pos(s);
                zeff[3 * i] = px;
                zeff[3 * i + 1] = py;
            }
        }
    }
    let zp: &[f64] = if zeff.is_empty() { z } else { &zeff };
    let pos = |i: usize| (zp[3 * i], zp[3 * i + 1]);
    let frozen = |i: usize| frz.map_or(false, |f| f[i].is_some());
    // dx/ds for a frozen square is 1 when it rides the high wall, 0 otherwise
    let dxds = |i: usize| -> (f64, f64) {
        match frz.and_then(|f| f[i]) {
            Some(fz) => (if fz.hix { 1.0 } else { 0.0 }, if fz.hiy { 1.0 } else { 0.0 }),
            None => (0.0, 0.0),
        }
    };
    cs.clear();
    for i in 0..n {
        let ang = match frz.and_then(|f| f[i]) {
            Some(fz) => fz.angle,
            None => z[3 * i + 2],
        };
        if tan_half && !frozen(i) {
            cs.push(dir_from_t(ang));
        } else {
            let (si, ci) = ang.sin_cos();
            cs.push((ci, si));
        }
    }
    // walls
    for i in 0..n {
        let (c, sn) = cs[i];
        let hh = h_cs(c, sn);
        let dhh = dh_cs(c, sn);
        let fz = frozen(i);
        let (ddx, ddy) = dxds(i);
        for d in 0..2 {
            let v = if d == 0 { pos(i).0 } else { pos(i).1 };
            let dvds = if d == 0 { ddx } else { ddy };
            let a = hh - v;
            if a > 0.0 {
                let (val, der) = shape(a, eps);
                e += val;
                if let Some(g) = g.as_deref_mut() {
                    if fz {
                        g[3 * n] -= der * dvds;
                    } else {
                        g[3 * i + d] -= der;
                        g[3 * i + 2] += der * dhh;
                    }
                }
            }
            let b = v + hh - s;
            if b > 0.0 {
                let (val, der) = shape(b, eps);
                e += val;
                if let Some(g) = g.as_deref_mut() {
                    if fz {
                        g[3 * n] += der * dvds;
                    } else {
                        g[3 * i + d] += der;
                        g[3 * i + 2] += der * dhh;
                    }
                    g[3 * n] -= der;
                }
            }
        }
    }
    // pairs
    let want = g.is_some();
    let pair = |i: usize, j: usize, e: &mut f64, g: &mut Option<&mut [f64]>| {
        let (fi, fj) = (frozen(i), frozen(j));
        if fi && fj {
            let (ix, iy) = dxds(i);
            let (jx, jy) = dxds(j);
            // Two frozen squares on the same walls keep their separation whatever
            // s does, so their term is a constant: skip it. Differently anchored
            // ones still approach each other as s shrinks, so they are kept.
            if ix == jx && iy == jy {
                return;
            }
        }
        let (ax, ay) = pos(i);
        let (bx, by) = pos(j);
        let dx = bx - ax;
        let dy = by - ay;
        if dx * dx + dy * dy >= 2.0 {
            return;
        }
        let (ac, as_) = cs[i];
        let (bc, bs) = cs[j];
        if let Some(hit) = pair_depth(ax, ay, ac, as_, bx, by, bc, bs, want) {
            let (val, der) = shape(hit.depth, eps);
            *e += val;
            if let Some(g) = g.as_deref_mut() {
                if fi {
                    let (ix, iy) = dxds(i);
                    g[3 * n] += der * (hit.grad[0] * ix + hit.grad[1] * iy);
                } else {
                    g[3 * i] += der * hit.grad[0];
                    g[3 * i + 1] += der * hit.grad[1];
                    g[3 * i + 2] += der * hit.grad[2];
                }
                if fj {
                    let (jx, jy) = dxds(j);
                    g[3 * n] += der * (hit.grad[3] * jx + hit.grad[4] * jy);
                } else {
                    g[3 * j] += der * hit.grad[3];
                    g[3 * j + 1] += der * hit.grad[4];
                    g[3 * j + 2] += der * hit.grad[5];
                }
            }
        }
    };
    match nbr {
        Some(nb) => {
            nb.ensure(zp, n);
            for i in 0..n {
                for &j in nb.of(i) {
                    pair(i, j as usize, &mut e, &mut g);
                }
            }
        }
        None => {
            for i in 0..n {
                for j in (i + 1)..n {
                    pair(i, j, &mut e, &mut g);
                }
            }
        }
    }
    // The gradient above is with respect to the angle; convert it to t.
    if tan_half {
        if let Some(g) = g.as_deref_mut() {
            for i in 0..n {
                if frozen(i) {
                    continue;
                }
                let t = z[3 * i + 2];
                g[3 * i + 2] *= 2.0 / (1.0 + t * t);
            }
        }
    }
    // Frozen slots are not free variables; make sure nothing moves them.
    if let Some(g) = g.as_deref_mut() {
        for i in 0..n {
            if frozen(i) {
                g[3 * i] = 0.0;
                g[3 * i + 1] = 0.0;
                g[3 * i + 2] = 0.0;
            }
        }
    }
    e
}

/// Maximum pairwise penetration depth (0 if no overlaps).
pub fn max_overlap(z: &[f64], n: usize) -> f64 {
    let cs: Vec<(f64, f64)> = (0..n).map(|i| {
        let (s, c) = z[3 * i + 2].sin_cos();
        (c, s)
    }).collect();
    let mut m: f64 = 0.0;
    for i in 0..n {
        for j in (i + 1)..n {
            let dx = z[3 * j] - z[3 * i];
            let dy = z[3 * j + 1] - z[3 * i + 1];
            if dx * dx + dy * dy >= 2.0 {
                continue;
            }
            if let Some(hit) = pair_depth(
                z[3 * i], z[3 * i + 1], cs[i].0, cs[i].1,
                z[3 * j], z[3 * j + 1], cs[j].0, cs[j].1, false,
            ) {
                m = m.max(hit.depth);
            }
        }
    }
    m
}

/// Side of the smallest axis-aligned square containing all the squares.
pub fn bbox(z: &[f64], n: usize) -> (f64, f64, f64, f64) {
    let (mut x0, mut y0, mut x1, mut y1) = (f64::INFINITY, f64::INFINITY, f64::NEG_INFINITY, f64::NEG_INFINITY);
    for i in 0..n {
        let (s, c) = z[3 * i + 2].sin_cos();
        let hh = h_cs(c, s);
        x0 = x0.min(z[3 * i] - hh);
        x1 = x1.max(z[3 * i] + hh);
        y0 = y0.min(z[3 * i + 1] - hh);
        y1 = y1.max(z[3 * i + 1] + hh);
    }
    (x0, y0, x1, y1)
}

/// Turn a nearly-feasible configuration into a strictly feasible one by scaling
/// the centers apart until no pair overlaps, then shrink-wrap the container.
/// Returns the certified side length (the configuration is updated in place).
pub fn make_feasible(z: &mut [f64], n: usize) -> f64 {
    let (x0, y0, x1, y1) = bbox(z, n);
    let (cx, cy) = ((x0 + x1) / 2.0, (y0 + y1) / 2.0);
    let orig: Vec<f64> = z.to_vec();
    let apply = |z: &mut [f64], f: f64| {
        for i in 0..n {
            z[3 * i] = cx + (orig[3 * i] - cx) * f;
            z[3 * i + 1] = cy + (orig[3 * i + 1] - cy) * f;
        }
    };
    if max_overlap(z, n) > 0.0 {
        let mut lo = 1.0;
        let mut hi = 1.0 + 1e-9;
        loop {
            apply(z, hi);
            if max_overlap(z, n) == 0.0 {
                break;
            }
            lo = hi;
            hi = 1.0 + (hi - 1.0) * 4.0;
            if hi > 2.0 {
                break;
            }
        }
        for _ in 0..60 {
            let mid = 0.5 * (lo + hi);
            apply(z, mid);
            if max_overlap(z, n) == 0.0 { hi = mid } else { lo = mid }
        }
        // small safety margin so rounding in re-evaluation cannot create overlap
        apply(z, hi * (1.0 + 1e-14));
    }
    let (x0, y0, x1, y1) = bbox(z, n);
    let side = (x1 - x0).max(y1 - y0);
    for i in 0..n {
        z[3 * i] -= x0;
        z[3 * i + 1] -= y0;
    }
    z[3 * n] = side;
    side
}

/// Normalize angles into [-pi/4, pi/4) (squares have 90-degree symmetry).
pub fn normalize_angles(z: &mut [f64], n: usize) {
    for i in 0..n {
        let t = z[3 * i + 2];
        z[3 * i + 2] = t - HALF_PI * ((t + HALF_PI / 2.0) / HALF_PI).floor();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn num_grad_check(z: &[f64], n: usize) {
        let mut cs = Vec::new();
        let mut g = vec![0.0; z.len()];
        energy(z, n, Some(&mut g), &mut cs);
        let eps = 1e-7;
        for k in 0..z.len() {
            let mut zp = z.to_vec();
            zp[k] += eps;
            let mut zm = z.to_vec();
            zm[k] -= eps;
            let num = (energy(&zp, n, None, &mut cs) - energy(&zm, n, None, &mut cs)) / (2.0 * eps);
            assert!((num - g[k]).abs() < 1e-5 * (1.0 + num.abs()), "k={k} num={num} ana={}", g[k]);
        }
    }

    #[test]
    fn gradient_matches_numeric() {
        let z = vec![0.6, 0.7, 0.3, 1.2, 1.1, -0.5, 1.5, 0.4, 0.1, 1.7];
        num_grad_check(&z, 3);
        let z = vec![0.4, 0.5, 0.05, 1.3, 0.6, 0.7, 1.0, 1.3, -0.2, 1.8];
        num_grad_check(&z, 3);
    }

    #[test]
    fn frozen_gradient_matches_numeric() {
        // Frozen squares ride the walls, so every one of their overlap terms has
        // to reach dE/ds instead of their own slots; a numeric check on s is the
        // only thing that catches a missing route.
        let n = 5;
        let s = 2.6;
        let mut z = vec![0.0; 3 * n + 1];
        let pts = [
            (0.55, 0.52, 0.0),
            (1.45, 0.60, 0.25),
            (0.60, 1.50, -0.3),
            (2.05, 2.05, 0.0),
            (1.40, 1.55, 0.4),
        ];
        for (i, p) in pts.iter().enumerate() {
            z[3 * i] = p.0;
            z[3 * i + 1] = p.1;
            z[3 * i + 2] = p.2;
        }
        z[3 * n] = s;
        // square 0 in the low corner, square 3 riding both high walls: the two
        // anchorings that must not be collapsed into a constant term
        let mut frz: Vec<Option<Frz>> = vec![None; n];
        frz[0] = Some(Frz { ox: z[0], oy: z[1], hix: false, hiy: false, angle: z[2] });
        frz[3] = Some(Frz { ox: s - z[9], oy: s - z[10], hix: true, hiy: true, angle: z[11] });
        let mut cs = Vec::new();
        let mut g = vec![0.0; 3 * n + 1];
        energy_frozen(&z, n, Some(&mut g), &mut cs, 0.0, None, false, Some(&frz));
        let h = 1e-7;
        for k in 0..z.len() {
            let mut zp = z.to_vec();
            zp[k] += h;
            let mut zm = z.to_vec();
            zm[k] -= h;
            let a = energy_frozen(&zp, n, None, &mut cs, 0.0, None, false, Some(&frz));
            let b = energy_frozen(&zm, n, None, &mut cs, 0.0, None, false, Some(&frz));
            let num = (a - b) / (2.0 * h);
            assert!(
                (num - g[k]).abs() < 1e-5 * (1.0 + num.abs()),
                "k={k} num={num} ana={}",
                g[k]
            );
        }
        // the overlap terms really are live, not all clipped away
        assert!(energy_frozen(&z, n, None, &mut cs, 0.0, None, false, Some(&frz)) > 0.0);
    }

    #[test]
    fn neighbour_list_matches_full_scan() {
        // A wrong neighbour list would silently change every energy, so the two
        // paths are held to bit-for-bit agreement on a jumbled configuration.
        let n = 40;
        let mut z = vec![0.0; 3 * n + 1];
        let mut s = 12345u64;
        let mut rnd = || {
            s = s.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            ((s >> 33) as f64) / ((1u64 << 31) as f64)
        };
        for i in 0..n {
            z[3 * i] = rnd() * 6.0;
            z[3 * i + 1] = rnd() * 6.0;
            z[3 * i + 2] = rnd() * 1.5;
        }
        z[3 * n] = 6.5;
        let mut cs = Vec::new();
        let mut nbr = Nbr::new();
        let mut g1 = vec![0.0; 3 * n + 1];
        let mut g2 = vec![0.0; 3 * n + 1];
        for step in 0..30 {
            // drift the squares so the list goes stale and has to rebuild
            for i in 0..n {
                // steady drift, so squares really do leave the skin and force rebuilds
                z[3 * i] += 0.02 + 0.01 * ((i + step) as f64).sin();
                z[3 * i + 1] += 0.015 * ((i * 2 + step) as f64).cos();
                z[3 * i + 2] += 0.01;
            }
            let a = energy_full(&z, n, Some(&mut g1), &mut cs, 0.0, None);
            let b = energy_full(&z, n, Some(&mut g2), &mut cs, 0.0, Some(&mut nbr));
            // The same pairs are summed in a different order, so agreement is to
            // rounding, not to the bit. A missing pair would show up far above this.
            assert!((a - b).abs() <= 1e-12 * a.abs().max(1.0), "energy differs at step {step}: {a} vs {b}");
            for k in 0..g1.len() {
                assert!(
                    (g1[k] - g2[k]).abs() <= 1e-12 * g1[k].abs().max(1.0),
                    "gradient[{k}] differs at step {step}: {} vs {}", g1[k], g2[k]
                );
            }
        }
        assert!(nbr.builds > 1, "list never rebuilt, test is not exercising staleness");
    }

    #[test]
    fn tan_half_matches_angle_parameterisation() {
        // Same geometry, different coordinates: the energy must be identical and
        // the gradient must differ exactly by the chain rule dtheta/dt = 2/(1+t^2).
        let n = 25;
        let mut z = vec![0.0; 3 * n + 1];
        let mut s = 987u64;
        let mut rnd = || {
            s = s.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            ((s >> 33) as f64) / ((1u64 << 31) as f64)
        };
        for i in 0..n {
            z[3 * i] = rnd() * 5.0;
            z[3 * i + 1] = rnd() * 5.0;
            z[3 * i + 2] = (rnd() - 0.5) * 1.2;
        }
        z[3 * n] = 5.5;
        let mut zt = z.clone();
        for i in 0..n {
            zt[3 * i + 2] = (z[3 * i + 2] * 0.5).tan();
        }
        let mut cs = Vec::new();
        let mut ga = vec![0.0; 3 * n + 1];
        let mut gt = vec![0.0; 3 * n + 1];
        let ea = energy_param(&z, n, Some(&mut ga), &mut cs, 0.0, None, false);
        let et = energy_param(&zt, n, Some(&mut gt), &mut cs, 0.0, None, true);
        assert!((ea - et).abs() <= 1e-12 * ea.abs().max(1.0), "energy differs: {ea} vs {et}");
        for i in 0..n {
            for d in 0..2 {
                let (a, b) = (ga[3 * i + d], gt[3 * i + d]);
                assert!((a - b).abs() <= 1e-12 * a.abs().max(1.0), "position gradient differs");
            }
            let tt = zt[3 * i + 2];
            let expect = ga[3 * i + 2] * 2.0 / (1.0 + tt * tt);
            let got = gt[3 * i + 2];
            assert!((expect - got).abs() <= 1e-12 * expect.abs().max(1.0),
                    "angle gradient differs: {expect} vs {got}");
        }
    }

    #[test]
    fn depth_axis_aligned() {
        let hit = pair_depth(0.0, 0.0, 1.0, 0.0, 0.9, 0.2, 1.0, 0.0, false).unwrap();
        assert!((hit.depth - 0.1).abs() < 1e-12);
        assert!(pair_depth(0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, false).is_none());
    }
}

/// Verlet neighbour lists: which squares are close enough to possibly touch.
///
/// The energy is dominated by the O(n^2) scan that rejects distant pairs, not by
/// the overlap kernel itself (measured at n=180: 28 of 46 microseconds). Two unit
/// squares can only overlap when their centres are within sqrt(2), so a list built
/// at sqrt(2) + skin stays valid until some square has moved by half the skin,
/// which during a line search is many evaluations.
pub struct Nbr {
    off: Vec<u32>,
    idx: Vec<u32>,
    at: Vec<(f64, f64)>,
    skin: f64,
    pub builds: u64,
    pub mode: NbrMode,
    order: Vec<u32>,
}

/// How the neighbour list is maintained. All three produce the same pairs; they
/// differ only in how often the work is redone.
#[derive(Clone, Copy, PartialEq, Debug)]
pub enum NbrMode {
    /// Cell grid, rebuilt only once a square has drifted past half the skin.
    Verlet,
    /// Cell grid, rebuilt on every evaluation. No skin, no staleness scan.
    Hash,
    /// Sort by x, then sweep forward while the x gap is under the cutoff.
    Sweep,
}

const R_CUT: f64 = std::f64::consts::SQRT_2;

impl Nbr {
    pub fn new() -> Self {
        let skin = std::env::var("SQ_SKIN").ok().and_then(|v| v.parse().ok()).unwrap_or(0.20);   // measured: flat between 0.15 and 0.35, worse outside
        let mode = match std::env::var("SQ_NBR").as_deref() {
            Ok("hash") => NbrMode::Hash,
            Ok("sweep") => NbrMode::Sweep,
            _ => NbrMode::Verlet,
        };
        Nbr { off: Vec::new(), idx: Vec::new(), at: Vec::new(), skin, builds: 0, mode, order: Vec::new() }
    }

    #[inline]
    fn stale(&self, z: &[f64], n: usize) -> bool {
        if self.at.len() != n {
            return true;
        }
        let half = 0.5 * self.skin;
        let h2 = half * half;
        for i in 0..n {
            let dx = z[3 * i] - self.at[i].0;
            let dy = z[3 * i + 1] - self.at[i].1;
            if dx * dx + dy * dy > h2 {
                return true;
            }
        }
        false
    }

    pub fn ensure(&mut self, z: &[f64], n: usize) {
        match self.mode {
            NbrMode::Verlet => {
                if self.stale(z, n) {
                    self.build(z, n);
                }
            }
            NbrMode::Hash => self.build(z, n),
            NbrMode::Sweep => self.build_sweep(z, n),
        }
    }

    /// Sweep and prune: sort the centres by x, then for each square walk forward
    /// while the x gap is under the cutoff. No grid, no cell size to pick, and it
    /// copes with uneven density, but it pays an O(n log n) sort every call.
    fn build_sweep(&mut self, z: &[f64], n: usize) {
        self.builds += 1;
        let r = R_CUT;
        self.order.clear();
        self.order.extend(0..n as u32);
        self.order.sort_unstable_by(|&a, &b| {
            z[3 * a as usize].partial_cmp(&z[3 * b as usize]).unwrap()
        });
        let mut lists: Vec<Vec<u32>> = vec![Vec::new(); n];
        for a in 0..n {
            let i = self.order[a] as usize;
            let xi = z[3 * i];
            let yi = z[3 * i + 1];
            for b in (a + 1)..n {
                let j = self.order[b] as usize;
                let dx = z[3 * j] - xi;
                if dx >= r {
                    break;
                }
                let dy = z[3 * j + 1] - yi;
                if dx * dx + dy * dy < r * r {
                    let (lo, hi) = if i < j { (i, j) } else { (j, i) };
                    lists[lo].push(hi as u32);
                }
            }
        }
        self.off.clear();
        self.idx.clear();
        for l in lists.iter() {
            self.off.push(self.idx.len() as u32);
            self.idx.extend_from_slice(l);
        }
        self.off.push(self.idx.len() as u32);
    }

    fn build(&mut self, z: &[f64], n: usize) {
        self.builds += 1;
        let r = R_CUT + self.skin;
        let (mut x0, mut y0) = (f64::INFINITY, f64::INFINITY);
        let (mut x1, mut y1) = (f64::NEG_INFINITY, f64::NEG_INFINITY);
        for i in 0..n {
            x0 = x0.min(z[3 * i]);
            x1 = x1.max(z[3 * i]);
            y0 = y0.min(z[3 * i + 1]);
            y1 = y1.max(z[3 * i + 1]);
        }
        // Cap the grid. A line search evaluates trial points that can fling a square
        // far away before the step is rejected, and sizing a dense grid from that
        // bounding box allocates unboundedly -- two runs reached 14 GB before this.
        // Coarser cells stay correct, since a 3x3 neighbourhood of cells at least r
        // wide still covers everything within r; they only cost extra candidates.
        let max_side = ((16 * n + 1024) as f64).sqrt().ceil().max(1.0);
        let cell = r.max(((x1 - x0).max(y1 - y0)) / max_side);
        let nx = (((x1 - x0) / cell).ceil() as usize + 1).max(1).min(max_side as usize + 1);
        let ny = (((y1 - y0) / cell).ceil() as usize + 1).max(1).min(max_side as usize + 1);
        let r = cell;
        let mut head = vec![u32::MAX; nx * ny];
        let mut next = vec![u32::MAX; n];
        let cell_of = |x: f64, y: f64| -> usize {
            let cx = (((x - x0) / r) as usize).min(nx - 1);
            let cy = (((y - y0) / r) as usize).min(ny - 1);
            cy * nx + cx
        };
        for i in 0..n {
            let c = cell_of(z[3 * i], z[3 * i + 1]);
            next[i] = head[c];
            head[c] = i as u32;
        }
        self.off.clear();
        self.idx.clear();
        self.at.clear();
        let r2 = r * r;
        for i in 0..n {
            self.off.push(self.idx.len() as u32);
            let (xi, yi) = (z[3 * i], z[3 * i + 1]);
            let cx = (((xi - x0) / r) as usize).min(nx - 1);
            let cy = (((yi - y0) / r) as usize).min(ny - 1);
            for gy in cy.saturating_sub(1)..=(cy + 1).min(ny - 1) {
                for gx in cx.saturating_sub(1)..=(cx + 1).min(nx - 1) {
                    let mut j = head[gy * nx + gx];
                    while j != u32::MAX {
                        let ju = j as usize;
                        if ju > i {
                            let dx = z[3 * ju] - xi;
                            let dy = z[3 * ju + 1] - yi;
                            if dx * dx + dy * dy < r2 {
                                self.idx.push(j);
                            }
                        }
                        j = next[ju];
                    }
                }
            }
        }
        self.off.push(self.idx.len() as u32);
        for i in 0..n {
            self.at.push((z[3 * i], z[3 * i + 1]));
        }
    }

    #[inline]
    pub fn of(&self, i: usize) -> &[u32] {
        &self.idx[self.off[i] as usize..self.off[i + 1] as usize]
    }
}

impl Default for Nbr {
    fn default() -> Self {
        Self::new()
    }
}
