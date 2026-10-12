#!/usr/bin/env node
// Headless runs of Ryan Xu's packing-lab engine (external/ry-xu/packing_lab.html,
// github.com/ry-xu/square_packing, pinned in external/ry-xu/COMMIT), unmodified.
//
// The page's own "auto" cycle, without a browser: random start of rounded
// squares (corner radius r), compression with shaking (walls only move inward),
// at jamming the rounding hardens to r = 0 in 14 joint solves, then the box
// tightens and compression of the true squares resumes. Repeats new starts
// until the deadline and writes the smallest valid packing found
// (lab check maxViolation <= 1e-8; certification happens elsewhere).
//
// usage: node compress_lab.js N SECONDS OUT [--seed S] [--round 20] [--lock]
//        [--wind off|seq] [--init FILE]   (FILE: our pose format, starts from it)
"use strict";
const fs = require("fs"), path = require("path"), vm = require("vm");

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const [N, SECONDS, OUT] = [parseInt(args[0]), parseFloat(args[1]), args[2]];
if (!N || !SECONDS || !OUT) { console.error("usage: node compress_lab.js N SECONDS OUT [options]"); process.exit(2); }

// Deterministic Math.random (mulberry32) so runs are reproducible from --seed.
let seed = (parseInt(opt("--seed", "1")) >>> 0) || 1;
const random = () => { seed = (seed + 0x6D2B79F5) >>> 0; let t = seed; t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };

const html = fs.readFileSync(path.join(__dirname, "external/ry-xu/packing_lab.html"), "utf8");
const m = html.match(/<script>([\s\S]*)<\/script>/);
if (!m) throw new Error("engine script not found");

// Minimal DOM: the controls' default values from the page, everything else inert.
const values = { "n-in": "55", speed: "6", wall: "45", shake: "40", round: opt("--round", "20"), wstr: "40" };
const checks = { fade: true, settle: true, lock: args.includes("--lock"), norot: false, "lock-outward": false, "repair-norot": true };
const noop = () => {};
const ctx2d = new Proxy({}, { get: (t, k) => (k in t ? t[k] : noop), set: (t, k, v) => { t[k] = v; return true; } });
const elements = {};
function element(id) {
  if (!elements[id]) elements[id] = { id, value: values[id] ?? "0", checked: !!checks[id], textContent: "", style: {}, dataset: {},
    hidden: true, width: 800, height: 800, clientWidth: 800, clientHeight: 800, className: "",
    classList: { add: noop, remove: noop, toggle: noop }, addEventListener: noop, setAttribute: noop, focus: noop, select: noop,
    getContext: () => ctx2d };
  return elements[id];
}
const sandbox = {
  Math: Object.create(Math, { random: { value: random } }), console, performance, Float64Array, Uint8Array, Int8Array,
  Array, Object, JSON, Number, String, Infinity, NaN, isFinite, parseInt, parseFloat, Proxy,
  document: { getElementById: element, querySelectorAll: () => [], documentElement: {}, addEventListener: noop, body: { classList: { add: noop, remove: noop } } },
  window: { devicePixelRatio: 1, addEventListener: noop }, addEventListener: noop,
  getComputedStyle: () => ({ getPropertyValue: () => "" }), requestAnimationFrame: noop,
  localStorage: { getItem: () => null, setItem: noop }, navigator: {},
};
vm.createContext(sandbox);

const driver = `
;(function () {
  globalThis.__headless = {
    start(N, init) {
      n = N; userRound = +document.getElementById("round").value; alloc(); setR(userRound / 100); ASP = 1;
      if (init) {
        setR(0); for (let i = 0; i < n; i++) { z[i] = init.x[i]; z[n + i] = init.y[i]; z[2 * n + i] = init.t[i]; } z[3 * n] = init.s;
      } else {
        const L = 2 * Math.sqrt(n) + 1; let k = 0, tries = 0;
        while (k < n && tries < 2000000) { tries++;
          const x = 0.75 + Math.random() * (L - 1.5), y = 0.75 + Math.random() * (L - 1.5), t = Math.random() * Math.PI / 2;
          let ok = true; for (let j = 0; j < k && ok; j++) if ((x - z[j]) ** 2 + (y - z[n + j]) ** 2 < 2.1) ok = false;
          if (ok) { z[k] = x; z[n + k] = y; z[2 * n + k] = t; k++; } }
        if (k < n) throw new Error("random start failed");
        z[3 * n] = L;
      }
      if (${JSON.stringify(opt("--wind", "off"))} === "seq") { wind = { mode: "seq" };
        windSeq = Array.from({ length: 20 }, () => WIND_OPTS[Math.floor(Math.random() * WIND_OPTS.length)]); }
      st = { ...S0, playing: true, auto: !init, wallStep: init ? wallMax() * 0.25 : wallMax(), phi0: phiNow() };
      lastValid = new Float64Array(z); PERM = null; setState("compress");
    },
    step() {          // one tick's worth of work, as in tick()
      if (st.state === "harden") { hardenStep(); if (st.state === "done" && st.auto) { tighten(); st.auto = false; } return; }
      resumeIfStopped(); if (st.state === "idle") setState("compress"); compressStep();
    },
    snapshot() { return { R, L: z[3 * n], viol: R === 0 ? maxViolation() : Infinity, z: Array.from(z), steps: st.steps, state: st.state }; },
  };
})();`;
vm.runInContext(m[1].replace(/\nnewStart\(\);\s*requestAnimationFrame\(tick\);\s*$/, "\n") + driver, sandbox, { filename: "packing_lab.js" });
const H = sandbox.__headless;

let init = null;
const initFile = opt("--init", null);
if (initFile) {
  const rows = fs.readFileSync(initFile, "utf8").split("\n").filter(l => l.trim() && !l.startsWith("#")).map(l => l.trim().split(/\s+/).map(Number));
  if (rows.length !== N) throw new Error(`init has ${rows.length} squares, expected ${N}`);
  let s = 0; for (const [x, y, t] of rows) { const h = (Math.abs(Math.cos(t)) + Math.abs(Math.sin(t))) / 2; s = Math.max(s, x + h, y + h); }
  init = { x: rows.map(r => r[0]), y: rows.map(r => r[1]), t: rows.map(r => r[2]), s: s * 1.0001 };
}

const deadline = Date.now() + SECONDS * 1000;
let best = null, starts = 0;
const log = [];
while (Date.now() < deadline) {
  H.start(N, init); starts++;
  let lastBestAt = Date.now(), runBest = Infinity;
  while (Date.now() < deadline) {
    H.step();
    const s = sandbox.__headless.snapshot();
    if (s.R === 0 && s.L < runBest - 1e-9 && s.viol <= 1e-8) {
      runBest = s.L; lastBestAt = Date.now();
      if (!best || s.L < best.L) { best = s; write(best); }
    }
    // A hardened run that has not improved for a while is finished; start over.
    if (s.R === 0 && Date.now() - lastBestAt > Math.max(15000, SECONDS * 100)) break;
  }
  log.push({ start: starts, best: runBest });
}
function write(b) {
  const n = N, lines = [];
  for (let i = 0; i < n; i++) lines.push(`${b.z[i]} ${b.z[n + i]} ${b.z[2 * n + i]}`);
  fs.writeFileSync(OUT + ".tmp", `# n = ${n}\n# s = ${b.L}\n# x y theta(rad)\n` + lines.join("\n") + "\n");
  fs.renameSync(OUT + ".tmp", OUT);
}
console.log(JSON.stringify({ n: N, starts, best: best ? best.L : null, runs: log }));
