# Record provenance and publication order

**October 18 intake update.** The current bound matrix and linked certificates include the verified October 18 intakes. The dated publication-order review below retains its historical scope. Later refinements do not transfer the discovery credit of their starting constructions.

Reviewed 17 October 2026. **No additional upper bound was found to import:** the records and pending precision supplements checked here are already retained. This review corrects source citations and records publication order; it changes no packing geometry or numerical bound.

The tables in this repository include imported packings, our refinements of other authors' packings, and our own constructions. A locally retained packing, a matching geometry or a tighter certificate does not establish that we discovered its underlying arrangement.

Machine-readable attribution and source references for **every n from 1 through 1024** are in [record_provenance.json](record_provenance.json). This is a dated review, bound to the listed source hashes, rather than a continuously updated claim of priority.

## Coverage

- Main at [`804eff369193b698d497a9c06847059eb9de0470`](https://github.com/jlevy/squares/commit/804eff369193b698d497a9c06847059eb9de0470).
- All **122 issues and 511 PRs**, open and closed, plus **1,105 issue/discussion comments**. PR line-review comments are a different GitHub endpoint and are not counted here.
- All **16 open PR heads**, fetched and compared by commit. None changed since the preceding intake.
- Metadata indexed for **8,022 main-history commits**, including **1,706 commits touching record-related paths**. This does not claim a manual reading of every historical code diff.
- **651 linked-source certificates**, **687 previously staged main/PR witnesses**, and **38 newer PR witness receipts**, compared with our exact retained bounds. The ten linked certificate repository heads are unchanged.
- PR #574's **147 numerical**, **60 algebraic**, and **2 earlier exact supplement** source hashes all match already retained submissions. These overlap and are not additive counts of new discoveries.
- **13 historic certificates** used for close priority comparisons passed fresh checks on both exact verifier routes.

The complete snapshots, extracted chronology, per-source comparisons and verification receipts are under `experiments/jlevy-provenance-20261017/`. The CSV contains 1,080 extracted upper-bound mentions; some quote older results and are expressly not treated as authorship claims. Local history contains 936 committed numerical candidate events.

## Reviewed findings

All times below are UTC. “First” means first in the reviewed evidence for the specified result, not an exhaustive worldwide priority assertion.

| Result | Date comparison | Credit conclusion |
| --- | --- | --- |
| Historical n=155 bound `12.952498944014007381965850566940` | Couzo certificate commit: **8 Oct 15:17:05**; [#451](https://github.com/jlevy/squares/issues/451): **8 Oct 15:53:07**. Daniel [#465](https://github.com/jlevy/squares/issues/465): **9 Oct 03:38:22**. | Couzo's refinement came first. Both certificates have exactly the same side and share **152 exact poses**. The starting construction remains SQUISH's. Jlevy [explicitly confirms this priority](https://github.com/jlevy/squares/issues/465#issuecomment-6116243324). |
| 8 October refinements at 108, 127, 131, 180 and 306 | Couzo [#451](https://github.com/jlevy/squares/issues/451): **8 Oct 15:53:07**; Mishapolk [#470](https://github.com/jlevy/squares/issues/470): **9 Oct 07:11:15**. | Our refinements were reported earlier, by 15 hours 18 minutes. The later table gives equal or slightly larger sides. Preserve Ryan Xu's starting constructions at 108/127/131, SQUISH and Siddharth Gupta at 180, and Couzo at 306. This does not assign us every later result at these counts. |
| Current n=132 Hunt 3 family, `11.9856801988458088…` | Daniel [#489](https://github.com/jlevy/squares/issues/489): **10 Oct 14:47:57**. Our earlier #476/#488 packings were larger. | Evan Daniel found this basin. Subsequent imports and precision work retain his discovery credit. #399 is not the report that introduced this result. |
| Current n=155, `12.952260944651` | Daniel [#669](https://github.com/jlevy/squares/issues/669): **17 Oct 14:49:46**. | A different local minimum found by Evan Daniel, starting from Daniil Ostashev's T-149 packing. This is separate from the earlier #451/#465 tie. |
| n=236, `15.861934390608` | SQUISH [#481](https://github.com/jlevy/squares/issues/481): **9 Oct**; Daniel [#659](https://github.com/jlevy/squares/issues/659): **16 Oct 14:05:14**. | SQUISH's Mondrian composition; Daniel reconstructed and further improved it. |
| n=271, `16.948947733714` | SQUISH [#500](https://github.com/jlevy/squares/issues/500): **11 Oct** → Couzo [#561](https://github.com/jlevy/squares/issues/561): **12 Oct** → Daniel [#664](https://github.com/jlevy/squares/issues/664): **17 Oct 04:30:51**. | SQUISH construction, followed by Couzo and Daniel refinements. Daniel explicitly calls this a refinement of #561. |
| 227, 229 and 260 Young-corner/slipped-ribbon packings | De Winter [#668](https://github.com/jlevy/squares/issues/668): **17 Oct 14:06:25**; our [#672](https://github.com/jlevy/squares/issues/672): **17 Oct 20:48:34**. | Joost de Winter found the constructions. Our subsequent 227/229 improvements retain that credit; 260 is an adopted source result. At 229 most of the later certified-bound reduction came from tighter certification, with only about `4.36e-11` of numerical geometric improvement. |
| De Winter's above-324 witnesses at 464, 509, 555, 603, 654, 706, 760, 817, 875, 935 and 998 | [#666](https://github.com/jlevy/squares/issues/666): **17 Oct 07:06:07**, before their import here. | De Winter's submitted results retain his credit and the Arslanov–Mustafin–Shangitbayev staircase/four-block method credit. Later improvements here keep that lineage. |

## 211 and 241: arrangement order differs from certificate order

These counts demonstrate why comparing issue creation dates alone gives an incomplete answer:

1. Our refined numerical arrangements were committed at **13 October 13:53:57** (`45966700…`) and reported in [#583](https://github.com/jlevy/squares/issues/583) at **14:11:17**.
2. Mishapolk's matching tighter exact certificates were committed in `8bb41af` at **15:51:54**.
3. Our matching precision certificates were committed in `b85dee2b964e7f7fb9f765227e60c44cdcd3aa4d` at **17:30:53** and reported in [#586](https://github.com/jlevy/squares/issues/586) at **17:37:01**.
4. Mishapolk's issue [#593](https://github.com/jlevy/squares/issues/593) followed at **14 October 01:40:32**.

Our arrangements were reported first; Mishapolk committed the matching tighter certificate before our precision commit. Both continue **Daniil Ostashev's constructions**. The matching exact sides were freshly checked here. Jlevy's [first comparison](https://github.com/jlevy/squares/issues/593#issuecomment-6163849805) records the commit ordering, while the [later registration decision](https://github.com/jlevy/squares/issues/593#issuecomment-6173398773) gives the earlier issue precedence under the project's reporting rule. These are different questions and should remain separate.

## Precision and derivative work

Mishapolk's `70a033f` update has twelve further exact refinements at 129, 154, 156, 175, 176, 204, 232, 264, 271, 302, 303 and 304. Jlevy's [per-count explanation](https://github.com/jlevy/squares/issues/593#issuecomment-6185872048) preserves Ostashev's packing credit at 129/175/176/204/232/264/303/304 and our arrangement/refinement credit at 154/156/271/302, together with the seed lineages preceding our work. A smaller exact certificate earns precision credit without becoming a new construction discovery.

Likewise, [PingYou's PR #574](https://github.com/jlevy/squares/pull/574) explicitly preserves earlier construction and refinement authors. Its 148 cumulative counts are not 148 newly discovered nominal packings. All its supplements were already imported here, including their original-credit metadata.

Our [#607](https://github.com/jlevy/squares/issues/607) explicitly attributes the composites at 703, 812, 930, 931, 992, 993 and 994 to **Kevin Fang**. Regenerating their certificates and independently verifying them does not transfer construction credit. Later lower bounds at the same counts are separate results.

## Citation corrections and limits

The importer now cites **#669 for `s155_ex2*`, #659 for `s236_bm3c*`, and #664 for `s271_ex1*`**, instead of allowing those newer candidate files to fall back to #399. Their credit labels preserve the stated starting construction/seed authors. Existing comparison entries at 155 and 236 were corrected immediately; the 271 comparison already had its specific citation.

`known_best.json`'s `also_found_by` lists geometric matches. A match can be an imported copy, shared seed, exact re-solve, independent rediscovery or another representative of the same packing. That field alone does not establish independence or priority.

Current issue bodies can contain later edits, and comments often quote other authors. Commit author/committer times and local job starts also do not independently prove the time of discovery or public availability. The reviewed findings above combine dates with pinned certificates, explicit lineage and maintainer comparisons. Other counts retain their source metadata without inventing an unsupported original finder.

## Later authorship clarification

Evan Daniel’s [authorship-correction request #673](https://github.com/jlevy/squares/issues/673) distinguishes finding a different local minimum from refining a packing within the same minimum. His request concerns 146 and 308. A seed citation alone should not be read as assigning authorship of the later minimum.
