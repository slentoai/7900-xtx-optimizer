# RX 7900 XTX Open Atlas Data

Maintainer: Craig Hasselbring

This folder is a standalone data-only release extracted from the private
`rdna3-discovery` workspace, plus a demo optimization layer for routing
application launches through atlas-backed RDNA3 runtime policies.

## Included Data

- `rx7900xtx_atlas.db`: SQLite database of 7900 XTX atlas measurements and invariants.
- `schema.sql`: SQLite schema for the atlas database.
- `atlas_export.json.gz.gz`: JSON export of the atlas data.
- `gfx1100_atlas_profile.json`: compact profile summary for the 7900 XTX / gfx1100 target.
- `rdna3_optimization_guide.json`: machine-readable optimization guidance derived from the atlas.
- `rdna3_optimization_guide.md`: markdown version of the optimization guide.
- `rdna3_atlas_constants.h`: generated constants header derived from the atlas data.

## Demo Optimization Layer

The `rdna3_optimization_layer/` package provides:
- RDNA3 GPU autodetection on Linux and Windows
- policy derivation from the 7900 XTX atlas
- conservative driver/runtime environment injection before launch
- a demo app showing how launched applications consume the policy

Quick start is documented in [GETTING_STARTED.md](GETTING_STARTED.md).

## Intentionally Excluded

- discovery engine code
- swarm logic
- kernel sources and compilers
- orchestration and mesh code
- benchmark runners
- profiling automation
- intermediate checkpoints, caches, and private tooling

## Notes

- The SQLite database contains three tables: `data_points`, `invariants`, and `discovery_sessions`.
- This package is intended to let you publish the measured 7900 XTX atlas data without publishing the discovery tool itself.
- The optimization layer is a user-space demo and does not modify the AMD kernel driver.
