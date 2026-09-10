# Historical tensor package

This directory retains the historical tensor implementation and tests from
the frozen research package. The independent audit found that its test suite
could not collect because required scripts and committed result inputs had
been omitted. Those inputs were restored from frozen commit
`2b7663bbf5a06d1340973434f195a84ae2773e8f`; no newly fitted data was substituted
for its regression inputs. `packaging_repair_manifest.json` in the root audit
evidence records the copied files and hashes.

The historical source readings and literature maps here are not the repaired
canonical J10–J12 definitions. Use the repository root, or the new portable
package in `release/classification`, for the corrected source evaluator and
exact source certificate. The root `INDEPENDENT_AUDIT.md` records both failed
and successful test runs and the bounds of the independent graph proof.
