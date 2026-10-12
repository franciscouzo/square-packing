#!/usr/bin/env python3
"""Rebuild the README table and image list from the packings on disk.

Values are measured with `sqpack verify` rather than read from each file's
header, and a packing that does not verify at zero overlap aborts the rebuild --
a stale or optimistic `# s =` line must never reach the table. Only the table
rows and the image list are touched; the prose is left alone.
"""
import glob, json, re, subprocess, sys
from pathlib import Path
from expanded_comparisons import PUBLISHED_MAX, render as render_expanded

BIN = "./target/release/sqpack"

cat = {}
for line in open("records.txt"):
    if line.startswith("#"):
        continue
    p = line.split()
    if len(p) == 2:
        cat[int(p[0])] = p[1]

rows, expanded_rows, gains = [], [], []
for f in sorted(glob.glob("n*.txt"), key=lambda p: int(re.search(r"n(\d+)\.txt", p).group(1))):
    n = int(re.search(r"n(\d+)\.txt", f).group(1))
    out = subprocess.run([BIN, "verify", f], capture_output=True, text=True).stdout
    if "max_pair_overlap=0.000e0" not in out:
        sys.exit(f"{f} does not verify; README not touched")
    side = float(re.search(r"bbox_side=([0-9.]+)", out).group(1))
    c = cat[n]
    if side >= float(c):
        sys.exit(f"{f} no longer beats the catalogue; README not touched")
    (rows if n <= PUBLISHED_MAX else expanded_rows).append(
        f"| {n} | {c} | **{side:.12f}** | {float(c)-side:.3e} |")
    if n <= PUBLISHED_MAX:
        gains.append((float(c) - side, n))

t = open("README.md").read()
start = t.index("| n | previous best known |")
end = t.index("\n\n", start)
head = t[start:t.index("\n", t.index("\n", start) + 1) + 1]
new = t[:start] + head + "\n".join(rows) + t[end:]
marker = "<!-- expanded-search-results -->"
end_marker = "<!-- /expanded-search-results -->"
known_path = Path("known_best.json")
known = json.loads(known_path.read_text()) if known_path.exists() else {}
expanded = render_expanded(expanded_rows, known)
if marker in new:
    a, b = new.index(marker), new.index(end_marker)+len(end_marker)
    new = new[:a]+expanded+new[b:]
elif Path("expanded_reference_bounds.json").exists():
    new += "\n"+expanded+"\n"
# Current standing: the comparison above is frozen to the September catalogue;
# known_best.json (import_external.py) holds the register and pending verified
# certificates by others.
status_marker, status_end = "<!-- current-status -->", "<!-- /current-status -->"
if known_path.exists():
    status_rows, counts = [], {}
    for row in rows:
        n, side = int(row.split("|")[1]), float(row.split("**")[1])
        e = known["entries"].get(str(n))
        if not e:
            continue
        other, source = e["side"], e["source"]
        if e.get("external") and source != "register" and not (e["register"] and e["register"]-other < 1e-9):
            who = f"[{e['external']['credit']}]({e['external']['request']})"
            who += " (pending)" if e["external"]["pending"] else ""
        else:
            who = "register"
        if side < other-1e-10:
            status, kind = "**best known**", "best known"
        elif side <= other+1e-10 and "Francisco Couzo" in (e.get("register_found_by") or []) and source == "register":
            # The register lists this very packing at its exact optimum.
            polish = e.get("register_improved_by") or []
            status = "**registered**" + (f" (exact optimum by {', '.join(polish)})" if polish else "")
            kind = "registered"
        elif side <= other+1e-10:
            status, kind = "tied (rounding)", "tied"
        else:
            status, kind = f"superseded by {side-other:.1e}", "superseded"
        counts[kind] = counts.get(kind, 0)+1
        lineage = ""
        cert = Path("found")/f"n{n}_s{side:.12f}.certificate.json"
        metadata = Path("certificates")/f"n{n}.json"
        if cert.exists() or metadata.exists():
            record = (json.loads(cert.read_text()) if cert.exists()
                      else json.loads(metadata.read_text()).get("origin", {}))
            job = record.get("search_job") or {}
            if record.get("seed_credit") or job.get("source_origin") == "external" \
                    or "external/seeds/" in str(job.get("source") or ""):
                credit = (record.get("seed_credit")
                          or (e["external"]["credit"] if e.get("external") else "an external packing"))
                lineage = f" (seeded from {credit})"
        # Only matches of the installed packing: a match of one of our older
        # packings (found/nN_s<side>.txt) says nothing about this one.
        also = [a for a in e.get("also_found_by") or []
                if a.get("ours") == f"n{n}.txt"
                or abs(float(a.get("ours", "_s0.txt").split("_s")[1][:-4])-side) < 1e-9]
        if also:
            status += " (same packing also in " + ", ".join(
                f"[#{a['request'].rsplit('/', 1)[-1]}]({a['request']})" for a in also) + ")"
        status_rows.append(f"| {n} | {side:.12f}{lineage} | {other:.12f} | {who} | {status} |")
    summary = ", ".join(f"{counts[k]} {k}" for k in ("best known", "registered", "tied", "superseded") if k in counts)
    status_block = (status_marker+"\n\n## Standing against the current register\n\n"
                    f"The table above compares with the catalogue as fetched in September. Against the "
                    f"[jlevy/squares register](https://jlevy.github.io/squares/) and verified pending "
                    f"submissions by others (`known_best.json`, refreshed {known['generated'][:10]}): {summary}.\n\n"
                    "| n | found here | best known elsewhere | source | status |\n|---|---|---|---|---|\n"
                    + "\n".join(status_rows)+"\n\n"+status_end)
    if status_marker in new:
        a, b = new.index(status_marker), new.index(status_end)+len(status_end)
        new = new[:a]+status_block+new[b:]
    elif marker in new:
        a = new.index(marker)
        new = new[:a]+status_block+"\n\n"+new[a:]
    else:
        new += "\n"+status_block+"\n"
gains.sort(reverse=True)
top = [n for _, n in gains[:5]]
new = re.sub(r"(?:!\[n = \d+\]\(n\d+\.svg\)\n?)+",
             "\n".join(f"![n = {n}](n{n}.svg)" for n in top) + "\n", new)
if new != t:
    open("README.md", "w").write(new)
    print(f"README updated: {len(rows)} published comparisons, {len(expanded_rows)} derived comparisons, images {top}")
else:
    print(f"README already current ({len(rows)} published, {len(expanded_rows)} derived comparisons)")
