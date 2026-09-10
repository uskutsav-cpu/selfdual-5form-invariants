# JHEP Stage 0 --- live repository state

Generated 2026-08-01T19:13:12+00:00 by `scripts/emit_jhep_live_state.py`.
Every value below is read from the working tree, not from a prior report.

## Head

| field | value |
|---|---|
| branch | `research/maximal-chiral-four-form-program` |
| local HEAD | `a962e7f8111fe90cc02f5fb7760b5fd27db5a1d3` |
| subject | Second certified sample point at rank 81, and fix a stale-summary trap |
| committed | 2026-08-01T14:13:11-05:00 |
| remote | https://github.com/uskutsav-cpu/selfdual-5form-invariants.git |
| tracked files | 529 |
| stashes | none |

## Branches

### Local

- `degree10/checkpointed-trace-pipeline 30fd0f63a9806bd2479aaeb402162ddfaad391e6`
- `degree12/mac-exact-optimized de696cabc4c4c3f6ee755b2824fe67e92f7c305b`
- `fix/exact-canon-order-8 7ed4645b05294f31e80f73499dc284e20db330cc`
- `main e84339dd3c8b1264765b89dd496323d61af140fc`
- `research/maximal-chiral-four-form-program a962e7f8111fe90cc02f5fb7760b5fd27db5a1d3`
- `stress-flow/classification-through-degree12 3ed32805b38ce34216b34888f6539e3538e90fb9`
- `stress-flow/exact-low-degree-map 04175461fdd55142b17e2e1c4e2fedf2455453ac`

### Remote

- `origin e84339dd3c8b1264765b89dd496323d61af140fc`
- `origin/degree10/checkpointed-trace-pipeline 30fd0f63a9806bd2479aaeb402162ddfaad391e6`
- `origin/degree12/mac-exact-optimized de696cabc4c4c3f6ee755b2824fe67e92f7c305b`
- `origin/fix/exact-canon-order-8 7ed4645b05294f31e80f73499dc284e20db330cc`
- `origin/main e84339dd3c8b1264765b89dd496323d61af140fc`
- `origin/research/maximal-chiral-four-form-program 17d7537d708d3708979d9cbfcba6be84f73babd9`
- `origin/stress-flow/classification-through-degree12 3ed32805b38ce34216b34888f6539e3538e90fb9`
- `origin/stress-flow/exact-low-degree-map 04175461fdd55142b17e2e1c4e2fedf2455453ac`

## Tags

- `order10-verified-30fd0f6 12b65ba557e1725a610ded3e29aa42c9d26c9164`
- `prl-submission-package-v1 82ec944b79d61c3946e9488b56ec484416aa810c`
- `q10-freeze-v1 6e74182681c5b7ef7fd51084d5686a2c0ad5e7ab`
- `rank81-certificate-v1 2a9fd62a30c89c21adc0882995cb5dfafeb0468f`
- `rank81-certificate-v2 8b9df40d184b31541eae865ae32dd9bd0b356504`
- `spinor-trace-bridge-v1 3e73d28de90cafbebe0f2e5e448627764ac62f15`
- `tensor-spinor-equivalence-v1 6935783e21f6696b98e050e887bc42ee8d9703bc`

## Uncommitted paths

None.

## Result artifacts a JHEP claim reads

| artifact | status | bytes | sha256 (first 16) | tracked |
|---|---|---|---|---|
| `results/rank81/certificate.json` | PRESENT | 110888 | `caf9b66390fae2cb` | yes |
| `results/rank81/minor81_certificate.json` | PRESENT | 4530 | `745f36b55427656e` | yes |
| `spinor_trace_bridge/results/bridge_validation.json` | PRESENT | 7141 | `93db9f8af7c6f25d` | yes |
| `verification/COMMON_SAMPLE_REGISTRY.json` | PRESENT | 208923 | `5095d6c3bb8e11f4` | yes |
| `results/10d_order8.json` | PRESENT | 7538 | `e780f0972fb8bfcf` | yes |
| `results/10d_order10.json` | PRESENT | 15684 | `92b02433d82e641c` | yes |
| `results/10d_order12.json` | PRESENT | 134920 | `9a784dc56a2bc818` | yes |
| `results/10d_graph_catalog.json` | PRESENT | 144435 | `a9ecaf225b2dac4c` | yes |
| `results/stress_flow_exact_low_degree.json` | PRESENT | 206723 | `98f8bd513bbb5c06` | yes |
| `results/live_state.json` | PRESENT | 2730 | `13d402cbad1550f7` | no |

Regeneration commands and what each artifact certifies are in
`audit/JHEP_RESULT_INVENTORY.json`.

## Test suites

### tensor side

    python -m pytest tests/ -q

23 test files.

### bridge side

    cd spinor_trace_bridge && python -m pytest

2 test files.

