# Shared packing store

CT105's `/var/lib/square-packing/database.sqlite3` is the authority for live
packings, exact bounds, immutable seeds, certificates and submission receipts.
The browser and native searches use the same transactional `tasks`, `seeds`,
`jobs` and `records` tables. A strictly smaller exact bound wins, including
gains below floating-point precision. A concurrent stronger result is preserved.

## Readers

- `GET /api/packings` lists all 10,000 current entries, including retired and
  proven-optimal counts. It supports ETag revalidation and gzip.
- `GET /api/packings/N` reads one current entry directly from the database.
- Each entry includes its exact `rational_target` and immutable `seed_url`.
  Downloads are checked against their SHA-256 on native clients.
- Search scheduling still uses `/api/tasks`; viewing a packing never changes
  its scheduling weight.

The LAN endpoint is `https://square-packing.franciscouzo.com` on CT105. Native
clients connect to `192.168.0.105` while verifying that HTTPS hostname and its
certificate. The local, ignored `packing_store.json` configures the connection.
Desktopo has a read-only client configuration. The CT104 coordinator sends the
chosen packing in each job, and Desktopo can also read current donor seeds.

`experiments/packing-cache/` holds disposable, immutable working copies and
receipts. Native clients refresh the catalogue every five seconds; the chart
refreshes all entries every twenty seconds and reads selected packings directly.
Running searches keep their existing starting arrangement until the next job.

## Acceptance and recovery

Native results go through the SSH-only `square-packing-web/ops/native_store.py`
gateway on CT105. It runs exact verification there and commits through the same
store used by the web API. The coordinator retains its durable `ready` item and
Desktopo retains its completed result until a final receipt is returned. Failed
connections are retried. Receipts are idempotent, and expired leases can be
recovered by the existing verifier. Telegram delivery remains on the existing
notification queue after central acceptance.

New jobs wait when the authoritative catalogue cannot be refreshed. They do not
silently choose a different record from an older repository copy.

Reviewed native certificates can be imported without redilating decimal poses.
Their original exact bytes are replayed with the retained rational verifier;
the migration therefore preserves improvements smaller than a float ulp.

## Git snapshots and public intake

Repository `n*.txt`, certificates and JSON indexes are reviewable Git snapshots.
They are exported and updated during explicit record intake. Live acceptance
does not rewrite the repository's record heads or require an rsync to the web
app. Historical basins remain available as deliberate alternative search starts.

After a reviewed public/record intake has copied its certificates and reference
geometry into `/var/lib/square-packing-campaign`, import it explicitly on CT105:

```sh
python3 /opt/square-packing-web/ops/bootstrap_packing_store.py \
  --root /var/lib/square-packing-campaign
```

This checks reference and certificate hashes, fills missing entries, compares
exact fractions and preserves stronger live results. It does not start searches.
The API service runs with `--central-store`; periodic campaign-file imports are
disabled. Keep that flag when changing its systemd command.

The initial migration and validation are recorded in
`experiments/central-store-20261022/`. The database and previous application files
were backed up under `/var/lib/square-packing-backups/central-store-20261022`.
