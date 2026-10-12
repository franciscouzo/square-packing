//! Minimal L-BFGS with backtracking (Armijo) line search.

pub struct Lbfgs {
    pub evals: usize,
    m: usize,
    s: Vec<Vec<f64>>,
    y: Vec<Vec<f64>>,
    rho: Vec<f64>,
    alpha: Vec<f64>,
    d: Vec<f64>,
    g: Vec<f64>,
    gn: Vec<f64>,
    zn: Vec<f64>,
}

impl Lbfgs {
    pub fn new(dim: usize, m: usize) -> Self {
        Lbfgs {
            evals: 0,
            m,
            s: vec![vec![0.0; dim]; m],
            y: vec![vec![0.0; dim]; m],
            rho: vec![0.0; m],
            alpha: vec![0.0; m],
            d: vec![0.0; dim],
            g: vec![0.0; dim],
            gn: vec![0.0; dim],
            zn: vec![0.0; dim],
        }
    }

    /// Minimize f starting from z (updated in place). `f(z, g)` returns the
    /// value and writes the gradient. Stops after 5 consecutive iterations that
    /// decrease f by less than `tol`. Returns the final value.
    pub fn minimize<F>(&mut self, z: &mut [f64], max_iter: usize, tol: f64, mut f: F) -> f64
    where
        F: FnMut(&[f64], &mut [f64]) -> f64,
    {
        let dim = z.len();
        let mut fx = f(z, &mut self.g);
        self.evals += 1;
        let mut k = 0usize; // number of stored pairs
        let mut head = 0usize;
        let mut stall = 0;
        for _ in 0..max_iter {
            // two-loop recursion: d = -H g
            self.d.copy_from_slice(&self.g);
            for idx in 0..k {
                let j = (head + self.m - 1 - idx) % self.m;
                let a = self.rho[j] * dot(&self.s[j], &self.d);
                self.alpha[j] = a;
                axpy(-a, &self.y[j], &mut self.d);
            }
            if k > 0 {
                let j = (head + self.m - 1) % self.m;
                let gamma = dot(&self.s[j], &self.y[j]) / dot(&self.y[j], &self.y[j]);
                self.d.iter_mut().for_each(|v| *v *= gamma);
            } else {
                let gn = dot(&self.g, &self.g).sqrt().max(1e-300);
                let sc = (1e-2 / gn).min(1.0);
                self.d.iter_mut().for_each(|v| *v *= sc);
            }
            for idx in (0..k).rev() {
                let j = (head + self.m - 1 - idx) % self.m;
                let b = self.rho[j] * dot(&self.y[j], &self.d);
                axpy(self.alpha[j] - b, &self.s[j], &mut self.d);
            }
            self.d.iter_mut().for_each(|v| *v = -*v);
            let mut gd = dot(&self.g, &self.d);
            if gd >= 0.0 {
                // not a descent direction: reset to steepest descent
                k = 0;
                let gn = dot(&self.g, &self.g).sqrt().max(1e-300);
                let sc = (1e-2 / gn).min(1.0);
                for i in 0..dim {
                    self.d[i] = -self.g[i] * sc;
                }
                gd = dot(&self.g, &self.d);
                if gd >= 0.0 {
                    break;
                }
            }
            // backtracking line search
            let mut step = 1.0;
            let mut fnew;
            let mut ok = false;
            loop {
                for i in 0..dim {
                    self.zn[i] = z[i] + step * self.d[i];
                }
                fnew = f(&self.zn, &mut self.gn);
                self.evals += 1;
                if fnew <= fx + 1e-4 * step * gd {
                    ok = true;
                    break;
                }
                step *= 0.5;
                if step < 1e-20 {
                    break;
                }
            }
            if !ok {
                if k == 0 {
                    break;
                }
                k = 0; // drop history and retry with steepest descent
                continue;
            }
            // update history
            let j = head;
            for i in 0..dim {
                self.s[j][i] = self.zn[i] - z[i];
                self.y[j][i] = self.gn[i] - self.g[i];
            }
            let sy = dot(&self.s[j], &self.y[j]);
            if sy > 1e-300 {
                self.rho[j] = 1.0 / sy;
                head = (head + 1) % self.m;
                k = (k + 1).min(self.m);
            }
            z.copy_from_slice(&self.zn);
            self.g.copy_from_slice(&self.gn);
            let dec = fx - fnew;
            fx = fnew;
            if dec < tol {
                stall += 1;
                if stall >= 5 {
                    break;
                }
            } else {
                stall = 0;
            }
        }
        fx
    }
}

// The two-loop recursion runs 2m dot products and 2m axpys over 3n+1 doubles every
// iteration, which profiling put at roughly 60% of a solve at n = 300 once the
// neighbour lists had taken the geometry down. Both are pure streaming loops, so
// they vectorize cleanly; two accumulators keep the multiply-add pipeline busy.
use std::simd::num::SimdFloat;
use std::simd::f64x4;

#[inline]
fn dot(a: &[f64], b: &[f64]) -> f64 {
    let n = a.len();
    let (mut acc0, mut acc1) = (f64x4::splat(0.0), f64x4::splat(0.0));
    let mut i = 0;
    while i + 8 <= n {
        acc0 += f64x4::from_slice(&a[i..]) * f64x4::from_slice(&b[i..]);
        acc1 += f64x4::from_slice(&a[i + 4..]) * f64x4::from_slice(&b[i + 4..]);
        i += 8;
    }
    while i + 4 <= n {
        acc0 += f64x4::from_slice(&a[i..]) * f64x4::from_slice(&b[i..]);
        i += 4;
    }
    let mut s = (acc0 + acc1).reduce_sum();
    while i < n {
        s += a[i] * b[i];
        i += 1;
    }
    s
}

#[inline]
fn axpy(a: f64, x: &[f64], y: &mut [f64]) {
    let n = x.len().min(y.len());
    let va = f64x4::splat(a);
    let mut i = 0;
    while i + 8 <= n {
        let y0 = f64x4::from_slice(&y[i..]) + va * f64x4::from_slice(&x[i..]);
        let y1 = f64x4::from_slice(&y[i + 4..]) + va * f64x4::from_slice(&x[i + 4..]);
        y0.copy_to_slice(&mut y[i..]);
        y1.copy_to_slice(&mut y[i + 4..]);
        i += 8;
    }
    while i + 4 <= n {
        let y0 = f64x4::from_slice(&y[i..]) + va * f64x4::from_slice(&x[i..]);
        y0.copy_to_slice(&mut y[i..]);
        i += 4;
    }
    while i < n {
        y[i] += a * x[i];
        i += 1;
    }
}
