#!/usr/bin/env python3
"""Refresh the best-known comparison table and external seed packings.

Sources (each pinned to the commit fetched, recorded in known_best.json):

- jlevy/squares register: the reported upper bound of every n <= 324
  (packing/frontier/STATUS.md);
- certified packings published by others: SQUISH (itsnaka/squish-certs),
  ry-xu/square_packing, Evan Daniel's candidates and his 5 October copy of
  every register packing (evand/square-packing), SidG2k1's refinements,
  Mishapolk's packings (jlevy/squares#470; decimal files, turned into exact
  rational witnesses here by a 1+1e-12 dilation, or a larger one if needed),
  Kevin Fang's (TheSnakeFang/squarepack-certs, #484), ebdeleeuw's n = 70
  refinement (#483), Daniil Ostashev's (dostashev/square-packing, #501),
  BuddenPing's (BuddenPing/square-packing-certificates, #503, #504) and
  Robert Barnett's refinements (RobertBarnettProjects/square-packing-research,
  #505).

An external packing geometrically identical to one of ours (aligned RMS
corner displacement < 1e-6) is recorded as "also found by", not as a
competitor; values within 1e-9 of each other keep the credit of the earlier
source (PRIORITY).

Writes known_best.json (tracked: values, sources and credit only) and, under
the ignored external/seeds/, decimal pose files in this repository's format:

  external/seeds/nN.txt          the best external packing, when it beats ours
  external/seeds/old/nN_TAG.txt  other basins: earlier register packings and
                                 superseded external packings, for the "old"
                                 search method

A packing becomes a seed only after its exact certificate passes
verify.py (sqpack.verify) in rational arithmetic; verdicts are cached by the
certificate's SHA-256 in external/seeds/verified.json. Third-party packings
are seeds and comparison bounds only: nothing here installs a record.

Usage: python3 import_external.py [--offline] [--no-verify]
"""
import argparse
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import time
import urllib.request
from expanded_comparisons import reviewed_publications

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT/"external/sources"
SEEDS = ROOT/"external/seeds"
REPOS = {
    "squish": "https://github.com/itsnaka/squish-certs.git",
    "ry-xu": "https://github.com/ry-xu/square_packing.git",
    "evand": "https://github.com/evand/square-packing.git",
    "sidg2k1": "https://github.com/SidG2k1/square-packing-refinements.git",
    "mishapolk": "https://github.com/Mishapolk/square-packing-records.git",
    "snakefang": "https://github.com/TheSnakeFang/squarepack-certs.git",
    "ebdeleeuw": "https://github.com/ebdeleeuw/square-packing-n70.git",
    "dostashev": "https://github.com/dostashev/square-packing.git",
    "buddenping": "https://github.com/BuddenPing/square-packing-certificates.git",
    "rbarnett": "https://github.com/RobertBarnettProjects/square-packing-research.git",
}
# Earlier, original constructors first: among values within ROUNDING of each
# other, credit goes to the first source in this order.
PRIORITY = ["register", "squish", "ry-xu", "evand", "sidg2k1", "mishapolk", "snakefang", "ebdeleeuw",
            "dostashev", "buddenping", "rbarnett"]
ROUNDING = 1e-9
CREDIT = {
    "squish": ("Nate Chaoweeraprasit (SQUISH)", "https://github.com/jlevy/squares/issues/422"),
    "ry-xu": ("Ryan Xu", "https://github.com/jlevy/squares/issues/432"),
    "evand": ("Evan Daniel", "https://github.com/jlevy/squares/issues/399"),
    "sidg2k1": ("Nate Chaoweeraprasit (SQUISH), precision-refined by SidG2k1", "https://github.com/jlevy/squares/issues/438"),
    "mishapolk": ("Mishapolk", "https://github.com/jlevy/squares/issues/470"),
    "snakefang": ("Kevin Fang (TheSnakeFang)", "https://github.com/jlevy/squares/issues/484"),
    "ebdeleeuw": ("ebdeleeuw (precision refinement of Ryan Xu)", "https://github.com/jlevy/squares/issues/483"),
    "dostashev": ("Daniil Ostashev", "https://github.com/jlevy/squares/issues/501"),
    "buddenping": ("BuddenPing", "https://github.com/jlevy/squares/issues/503"),
    "rbarnett": ("Robert Barnett (refinement of Ryan Xu)", "https://github.com/jlevy/squares/issues/505"),
}
REGISTER = "https://raw.githubusercontent.com/jlevy/squares/{}/packing/frontier/STATUS.md"
# Registration requests by certificate, where a source has filed more than one.
REQUEST_BY_PATH = {"evand/search/packer/candidates/hunt1_": "https://github.com/jlevy/squares/issues/465",
                   "evand/search/packer/candidates/hunt3_": "https://github.com/jlevy/squares/issues/489",
                   "evand/search/packer/candidates/tt_n154": "https://github.com/jlevy/squares/issues/552",
                   "evand/search/packer/candidates/big1_n375.": "https://github.com/evand/square-packing/blob/31523f87316bdfda00f5459dd9077928e264f133/search/packer/PACKER.md#L957-L988",
                   "evand/search/packer/candidates/polish_n375.": "https://github.com/evand/square-packing/blob/31523f87316bdfda00f5459dd9077928e264f133/search/packer/PACKER.md#L942-L954",
                   "squish/squish-submission-2026-10-06/": "https://github.com/jlevy/squares/issues/401",
                   "squish/squish-submission-2026-10-07": "https://github.com/jlevy/squares/issues/422",
                   "squish/squish-submission-2026-10-09/": "https://github.com/jlevy/squares/issues/481",
                   "squish/squish-submission-2026-10-11/": "https://github.com/jlevy/squares/issues/500",
                   "buddenping/n153.": "https://github.com/jlevy/squares/issues/504",
                   "dostashev/records/n0175.": "https://github.com/jlevy/squares/issues/528",
                   "dostashev/records/n0232.": "https://github.com/jlevy/squares/issues/528",
                   "dostashev/records/n0264.": "https://github.com/jlevy/squares/issues/528"}


def request_for(source, path):
    for prefix, url in REQUEST_BY_PATH.items():
        if str(path).startswith(prefix):
            return url
    return CREDIT[source][1]


def credit_for(source, path):
    if str(path).startswith('evand/search/packer/candidates/tt_n154'):
        return 'Evan Daniel (from Francisco Couzo\'s n=155 seed)'
    if str(path).startswith('evand/search/packer/candidates/hunt3_n34'):
        return 'Evan Daniel (after Kevin Fang)'
    if str(path).startswith(('evand/search/packer/candidates/big1_n375.',
                             'evand/search/packer/candidates/polish_n375.')):
        return 'Evan Daniel (from a Francisco Couzo seed)'
    return CREDIT[source][0]


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.strip()


def fetch(offline):
    commits = {}
    SOURCES.mkdir(parents=True, exist_ok=True)
    for name, url in REPOS.items():
        path = SOURCES/name
        if not offline:
            if path.exists():
                git("-C", str(path), "fetch", "-q", "--depth", "1", "origin", "HEAD")
                git("-C", str(path), "reset", "-q", "--hard", "FETCH_HEAD")
            else:
                git("clone", "-q", "--depth", "1", url, str(path))
        commits[name] = {"url": url, "commit": git("-C", str(path), "rev-parse", "HEAD")}
    status = SOURCES/"register-STATUS.md"
    if not offline:
        with urllib.request.urlopen("https://api.github.com/repos/jlevy/squares/commits/main") as r:
            sha = json.load(r)["sha"]
        with urllib.request.urlopen(REGISTER.format(sha)) as r:
            status.write_bytes(r.read())
        (SOURCES/"register-commit.txt").write_text(sha+"\n")
    commits["register"] = {"url": "https://github.com/jlevy/squares",
                           "commit": (SOURCES/"register-commit.txt").read_text().strip()}
    return commits


def evaluate(expression):
    """Decimal value of a register bound such as `5 + (1/2)√2` or `root(P, 3.87...)`."""
    e = expression.strip().strip("`")
    m = re.match(r"root\([^,]+,\s*([0-9.]+)\)", e)
    if m:
        return float(m[1])
    if re.fullmatch(r"\d+/\d+", e):
        return float(Fraction(e))
    e = re.sub(r"(?<=[\d)])\s*√", "*√", e)
    e = re.sub(r"√(\d+)", r"math.sqrt(\1)", e)
    if not re.fullmatch(r"[0-9.()+\-*/ mathsqrt]+", e):
        raise ValueError(f"unrecognised register bound {expression!r}")
    return float(eval(e, {"math": math, "sqrt": math.sqrt}))


OWN_NAME = "Francisco Couzo"


def register_attribution(n, commit, offline):
    """found_by / improved_by of the register's reported upper bound for n."""
    cache = SOURCES/"register-cases"/commit/f"n-{n:03d}.md"
    if not cache.exists():
        if offline:
            return None
        cache.parent.mkdir(parents=True, exist_ok=True)
        try:
            with urllib.request.urlopen(f"https://raw.githubusercontent.com/jlevy/squares/{commit}/packing/frontier/n-{n:03d}.md") as r:
                cache.write_bytes(r.read())
        except OSError:
            return None
    text = cache.read_text()
    block = text[text.find("reported_upper_bound:"):text.find("verified_upper_bound:")]
    out = {}
    for key in ("found_by", "improved_by"):
        m = re.search(rf"\n\s+{key}:\n((?:\s+- .*\n)+)", block)
        out[key] = re.findall(r"- (.*)", m[1]) if m else []
    return out


def register_bounds():
    bounds = {}
    for line in (SOURCES/"register-STATUS.md").read_text().splitlines():
        m = re.match(r"\| \[`(\d+)`\]\([^)]*\) \| ([^|]*) \| ([^|]*) \|", line)
        if m:
            bounds[int(m[1])] = {"reported": evaluate(m[2]), "reported_text": m[2].strip().strip("`"),
                                 "verified_text": m[3].strip().strip("`")}
    if len(bounds) < 300:
        raise ValueError(f"register parse found only {len(bounds)} rows")
    return bounds


def read_cert_text(path):
    """Evan Daniel's .cert format: comment lines, 'n S', then 'x y t' rationals."""
    rows = [l.split() for l in path.read_text().splitlines() if l.strip() and not l.startswith("#")]
    n, side = int(rows[0][0]), Fraction(rows[0][1])
    return n, side, [tuple(map(Fraction, r[:3])) for r in rows[1:n+1]]


def read_sqcert(path):
    """Daniil Ostashev's .sqcert: comment lines, 'n N', 's S', then 'x y t' rationals."""
    rows = [l.split() for l in path.read_text().splitlines() if l.strip() and not l.startswith("#")]
    head = {r[0]: r[1] for r in rows[:2]}
    n, side = int(head["n"]), Fraction(head["s"])
    return n, side, [tuple(map(Fraction, r[:3])) for r in rows[2:n+2]]


def read_cert_json(path):
    d = json.loads(path.read_text())
    squares = [tuple(map(Fraction, (q["x"], q["y"], q["t"]) if isinstance(q, dict) else q))
               for q in d["squares"]]
    return d["n"], Fraction(d["s_exact"]), squares


def certificates():
    """Yield (n, side, squares, source, relative path) for every certificate found."""
    for path in sorted((SOURCES/"squish").glob("squish-submission-*/n*/n*.cert.json")):
        yield (*read_cert_json(path), "squish", path)
    for path in sorted((SOURCES/"ry-xu").glob("certificates/n*/n*.cert.json")):
        yield (*read_cert_json(path), "ry-xu", path)
    for path in sorted((SOURCES/"evand").glob("search/packer/candidates/*.cert")):
        yield (*read_cert_text(path), "evand", path)
    for path in sorted((SOURCES/"sidg2k1").glob("witnesses/packing-*.cert")):
        yield (*read_cert_text(path), "sidg2k1", path)
    for path in sorted((SOURCES/"snakefang").glob("n*/n*.cert")):
        yield (*read_cert_text(path), "snakefang", path)
    for path in sorted((SOURCES/"ebdeleeuw").glob("certificate.json")):
        d = json.loads(path.read_text())
        side = Fraction(d["side"])
        shift = side/2 if d.get("coordinate_system") == "centered" else 0
        squares = [(Fraction(q["x"])+shift, Fraction(q["y"])+shift, Fraction(q["t"])) for q in d["squares"]]
        yield d["n"], side, squares, "ebdeleeuw", path
    for path in sorted((SOURCES/"dostashev").glob("records/n*.sqcert")):
        yield (*read_sqcert(path), "dostashev", path)
    for path in sorted((SOURCES/"buddenping").glob("n*.cert.json")):
        yield (*read_cert_json(path), "buddenping", path)
    # Current results only (superseded/ holds their earlier versions); n <= 999.
    for path in sorted((SOURCES/"rbarnett").glob("certificates/n[0-9][0-9][0-9].cert")):
        yield (*read_cert_text(path), "rbarnett", path)


def decimal_packings():
    """Mishapolk's files: 's: S' then 'Square i: x=.., y=.., deg=..', box centred at 0."""
    for path in sorted((SOURCES/"mishapolk").glob("certificates/square-*.txt")):
        text = path.read_text()
        m = re.search(r"s:\s*([0-9.]+)", text)
        rows = re.findall(r"x=([-0-9.eE+]+), y=([-0-9.eE+]+), deg=([-0-9.eE+]+)", text)
        if not m or not rows:
            continue
        s = Fraction(m[1])
        poses = [(Fraction(x)+s/2, Fraction(y)+s/2, math.radians(float(d))) for x, y, d in rows]
        yield len(poses), poses, "mishapolk", path


def rational_witness(poses, grow):
    """Rational centres and t = tan(theta/2), centres scaled apart by `grow`
    about their mean, box shrink-wrapped; returns (side, squares)."""
    sq = [(x, y, Fraction(math.tan(th/2)).limit_denominator(10**12)) for x, y, th in poses]
    cx = sum(q[0] for q in sq)/len(sq)
    cy = sum(q[1] for q in sq)/len(sq)
    sq = [(cx+(x-cx)*grow, cy+(y-cy)*grow, t) for x, y, t in sq]
    pts = [p for q in sq for p in corners(*q)]
    x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
    sq = [(x-x0, y-y0, t) for x, y, t in sq]
    side = max(max(p[0]-x0, p[1]-y0) for p in pts)
    return side, sq


def corners(x, y, t):
    d = 1+t*t
    c, s = (1-t*t)/d, 2*t/d
    h = Fraction(1, 2)
    return [(x+dx*c-dy*s, y+dx*s+dy*c) for dx, dy in ((-h, -h), (h, -h), (h, h), (-h, h))]


def exact_check(args):
    side, squares = args
    from verify import verify_packing

    def sign(v):
        return (v > 0)-(v < 0)
    report = verify_packing([corners(*q) for q in squares], side, sign, bucket=True)
    return {"valid": report.valid, "pairs_tested": report.pairs_tested,
            "failures": [str(f) for f in report.failures[:3]]}


_OURS = {}


def same_as_ours(n, d):
    """The name of our archived packing that d is (aligned RMS < 1e-6), or None."""
    import numpy as np
    from normalize_findings import align
    side = float(d["side"])
    if n not in _OURS:
        files = [ROOT/f"n{n}.txt", ROOT/"superseded"/f"n{n}.txt", *sorted((ROOT/"found").glob(f"n{n}_s*.txt"))]
        _OURS[n] = []
        for f in files:
            if f.exists():
                try:
                    s = next(float(l.split("=")[1]) for l in f.read_text().splitlines() if l.startswith("# s ="))
                    _OURS[n].append((s, f))
                except StopIteration:
                    pass
    z = np.array([(float(x), float(y), 2*math.atan(float(t))) for x, y, t in d["squares"]])
    for s, f in _OURS[n]:
        if abs(s-side) > 1e-6:
            continue
        ref = np.loadtxt(f, comments="#", ndmin=2)
        if len(ref) != len(z):
            continue
        out, _ = align(z, ref)
        # Same packing up to rattlers: loose squares can sit anywhere without
        # changing the side, so allow a few squares to differ.
        a, b = wrap_xy(out), wrap_xy(ref)
        dxy = (a[:, :2]-a_side(a)/2)-(b[:, :2]-a_side(b)/2)
        dang = (a[:, 2]-b[:, 2]+np.pi/4) % (np.pi/2)-np.pi/4
        moved = np.sqrt(np.sum(dxy**2, axis=1)+1-np.cos(dang)) > 1e-5
        # Packings with many exact flat motions (loose squares) differ there;
        # equal sides plus a large common core is the same local minimum.
        if moved.sum() <= max(3, len(z)//30) or (abs(s-side) < 1e-9 and moved.sum() <= 0.15*len(z)):
            return f.name
    return None


def wrap_xy(z):
    from slp_refine import wrap
    return wrap(z)[0]


def a_side(z):
    import numpy as np
    h = (np.abs(np.cos(z[:, 2]))+np.abs(np.sin(z[:, 2])))/2
    return float(np.max(np.maximum(z[:, 0], z[:, 1])+h))


def own_sides():
    out = {}
    for path in ROOT.glob("n[0-9]*.txt"):
        for line in path.read_text().splitlines():
            if line.startswith("# s ="):
                out[int(path.stem[1:])] = float(line.split("=")[1])
    return out


def write_pose(path, side, squares):
    """Decimal seed file. Certificates with ~1e-20 gaps can overlap by ~1e-16
    once rounded to floats, so seeds pass through slp_refine.repair (which
    rechecks every pair) and are written at the repaired side."""
    import numpy as np
    from slp_refine import repair
    z = np.array([(float(x), float(y), 2*math.atan(float(t))) for x, y, t in squares])
    z, side = repair(z)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# n = {len(z)}\n# s = {side:.17g}\n# x y theta(rad)\n" +
                    "".join(f"{x:.17g} {y:.17g} {t:.17g}\n" for x, y, t in z))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--offline", action="store_true", help="use the sources already fetched")
    p.add_argument("--no-verify", action="store_true", help="skip exact checks (seeds are then not written)")
    p.add_argument("--procs", type=int, default=1)
    a = p.parse_args()
    import fcntl
    SOURCES.mkdir(parents=True, exist_ok=True)
    lock = (SOURCES/".import.lock").open("w")
    fcntl.flock(lock, fcntl.LOCK_EX)  # one import at a time (hourly refresh, notifications)
    commits = fetch(a.offline)
    register = register_bounds()
    own = own_sides()
    cache_path = SEEDS/"verified.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}

    # Best certificate per n, plus every other one as an alternative basin.
    found = {}
    for n, side, squares, source, path in certificates():
        if len(squares) != n:
            raise ValueError(f"{path}: {len(squares)} squares, header says {n}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        found.setdefault(n, []).append({"side": side, "squares": squares, "source": source,
                                        "path": str(path.relative_to(SOURCES)), "sha256": digest})
    for n, poses, source, path in decimal_packings():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        known = cache.get(digest)
        for k in ([known["grow_exp"]] if known and known.get("valid") else range(12, 7, -1)):
            side, squares = rational_witness(poses, 1+Fraction(1, 10**k))
            if not (known and known.get("valid")):
                if a.no_verify:
                    break
                verdict = exact_check((side, squares))
                if not verdict["valid"]:
                    cache[digest] = {**verdict, "path": str(path.relative_to(SOURCES)), "grow_exp": None}
                    continue
                cache[digest] = {**verdict, "path": str(path.relative_to(SOURCES)), "grow_exp": k,
                                 "checked": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
                print(f"  n={n} {path.name}: VALID at dilation 1+1e-{k}", flush=True)
            found.setdefault(n, []).append({"side": side, "squares": squares, "source": source,
                                            "path": str(path.relative_to(SOURCES)), "sha256": digest})
            break
        else:
            print(f"  n={n} {path.name}: no valid rational witness up to dilation 1+1e-8", flush=True)
    for n, items in found.items():
        # A packing no smaller than the trivial grid bound ceil(sqrt(n)) is no record.
        grid = math.isqrt(n-1)+1
        trivial = [d for d in items if d["side"] >= grid]
        for d in trivial:
            items.remove(d)
            print(f"  n={n} {d['path']}: side {float(d['side']):.12f} is not below the grid bound {grid}; ignored", flush=True)
        items.sort(key=lambda d: d["side"])

    todo = [d for items in found.values() for d in items if d["sha256"] not in cache]
    if todo and not a.no_verify:
        print(f"exactly verifying {len(todo)} certificates", flush=True)
        with ProcessPoolExecutor(a.procs) as pool:
            for d, verdict in zip(todo, pool.map(exact_check, [(d["side"], d["squares"]) for d in todo])):
                cache[d["sha256"]] = {**verdict, "path": d["path"], "checked": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
                print(f"  n={len(d['squares'])} {d['path']}: {'VALID' if verdict['valid'] else 'INVALID'}", flush=True)
        SEEDS.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache, indent=2)+"\n")

    entries = {}
    for n in sorted(set(register) | set(found)):
        reg = register.get(n)
        candidates = [d for d in found.get(n, []) if cache.get(d["sha256"], {}).get("valid")]
        also = []
        for d in list(candidates):
            ours = same_as_ours(n, d)
            if ours:
                candidates.remove(d)
                d["same_as_ours"] = ours
                also.append({"source": d["source"], "credit": credit_for(d["source"], d["path"]),
                             "request": request_for(d["source"], d["path"]), "ours": ours})
        best_ext = None
        if candidates:
            low = float(candidates[0]["side"])
            near = [d for d in candidates if float(d["side"]) <= low+ROUNDING]
            best_ext = min(near, key=lambda d: PRIORITY.index(d["source"]))
        options = []
        if reg:
            options.append((reg["reported"], "register"))
        if best_ext:
            options.append((float(best_ext["side"]), best_ext["source"]))
        if not options:
            continue  # only packings no better than the grid, or only copies of ours
        side = min(o[0] for o in options)
        source = min((o for o in options if o[0] <= side+ROUNDING), key=lambda o: PRIORITY.index(o[1]))[1]
        entry = {"side": side, "source": source,
                 "register": reg["reported"] if reg else None,
                 "register_text": reg["reported_text"] if reg else None}
        if also:
            entry["also_found_by"] = also
        if best_ext:
            who, url = credit_for(best_ext["source"], best_ext["path"]), request_for(best_ext["source"], best_ext["path"])
            entry["external"] = {"side": str(best_ext["side"]), "side_decimal": float(best_ext["side"]),
                                 "source": best_ext["source"], "credit": who, "request": url,
                                 "certificate": best_ext["path"], "sha256": best_ext["sha256"],
                                 "pending": reg is None or float(best_ext["side"]) < reg["reported"]-1e-12}
        if n in own and reg:
            who = register_attribution(n, commits["register"]["commit"], a.offline)
            if who:
                entry["register_found_by"] = who["found_by"]
                entry["register_improved_by"] = who["improved_by"]
        if n in own:
            entry["own"] = own[n]
            entry["own_status"] = ("best known" if own[n] < side-1e-10 else
                                   "tied (within 1e-10)" if own[n] <= side+1e-10 else "superseded")
        entries[str(n)] = entry

    # Seeds: the best external packing where it beats ours, every other
    # verified external packing as an alternative basin. Files are replaced
    # atomically and stale ones removed afterwards: the coordinator may be
    # reading them.
    wanted = {}
    for n, items in found.items():
        valid = [d for d in items if cache.get(d["sha256"], {}).get("valid") and not d.get("same_as_ours")]
        if not valid:
            continue
        best = valid[0]
        if float(best["side"]) < own.get(n, math.inf)-1e-9:
            wanted[SEEDS/f"n{n}.txt"] = (best["side"], best["squares"])
            entries[str(n)]["seed"] = f"external/seeds/n{n}.txt"
        for d in valid[1:]:
            wanted[SEEDS/"old"/f"n{n}_{d['source']}_{d['sha256'][:10]}.txt"] = (d["side"], d["squares"])
    # Evan Daniel's copy of every register packing on 5 October: the
    # pre-SQUISH basins. Float poses in his format (degrees), used as given.
    batch = SOURCES/"evand/search/exact/batch/inputs"
    for path in sorted(batch.glob("n-*.txt")):
        rows = [l.split() for l in path.read_text().splitlines() if l.strip() and not l.startswith("#")]
        n, side = int(rows[0][0]), float(rows[0][1])
        if abs(side-round(side)) < 1e-9 or n < 10:
            continue
        squares = [(Fraction(r[0]), Fraction(r[1]), Fraction(math.tan(math.radians(float(r[2]))/2)))
                   for r in rows[1:n+1]]
        wanted[SEEDS/"old"/f"n{n}_register-20261005.txt"] = (side, squares)
    for target, (side, squares) in wanted.items():
        tmp = target.with_name(target.name+".tmp")
        write_pose(tmp, side, squares)
        tmp.replace(target)
    for stale in list(SEEDS.glob("n[0-9]*.txt"))+list((SEEDS/"old").glob("*.txt")):
        if stale not in wanted:
            stale.unlink()

    manifest = {"generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "sources": commits,
                "note": "Best known upper bounds: the register's reported value or a verified, published "
                        "certificate. Third-party packings are credited to their authors and are used here only "
                        "as comparison bounds and search seeds.",
                "entries": entries,
                "published_above_324": reviewed_publications(found, cache, commits, credit_for, request_for)}
    tmp = ROOT/"known_best.json.tmp"
    tmp.write_text(json.dumps(manifest, indent=2)+"\n")
    tmp.replace(ROOT/"known_best.json")  # readers never see a partial file
    status = {}
    for e in entries.values():
        if "own_status" in e:
            status[e["own_status"]] = status.get(e["own_status"], 0)+1
    print(f"known_best.json: {len(entries)} counts; ours: {status}; "
          f"seeds: {len(list(SEEDS.glob('n[0-9]*.txt')))}, old basins: {len(list((SEEDS/'old').glob('*.txt')))}")


if __name__ == "__main__":
    main()
