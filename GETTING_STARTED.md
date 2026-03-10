# Getting Started

Maintainer: Craig Hasselbring

## What This Demo Does

This repository contains a data-only RX 7900 XTX atlas release plus a demo optimization layer.
The layer detects AMD RDNA3 GPUs, derives a runtime policy from the atlas, injects conservative
runtime and driver-facing environment variables, and launches an application through that policy.

This is a user-space launcher demo. It does not patch AMD kernel drivers or replace ROCm.
It shows how to route application launches through an atlas-backed optimization shim.

## Repository Layout

- `rx7900xtx_atlas.db`: atlas measurements and invariants
- `atlas_export.json.gz.gz`: JSON export of the atlas
- `rdna3_optimization_layer/`: Python package for detection, policy building, and launch
- `GETTING_STARTED.md`: quick-start instructions

## Linux Quick Start

1. Install Python 3.10+.
2. Optional: create a virtual environment.
3. Run detection:

```bash
python3 -m rdna3_optimization_layer detect
```

4. Print the environment that would be injected:

```bash
python3 -m rdna3_optimization_layer env
```

5. Dry-run a launch:

```bash
python3 -m rdna3_optimization_layer launch --dry-run -- python3 -m rdna3_optimization_layer.demo_app
```

6. Launch an application through the layer:

```bash
python3 -m rdna3_optimization_layer launch -- python3 -m rdna3_optimization_layer.demo_app
```

Example with a real program:

```bash
python3 -m rdna3_optimization_layer launch -- ./my_app --model resnet50
```

## Windows Quick Start

1. Install Python 3.10+.
2. Open PowerShell in the repository directory.
3. Run detection:

```powershell
py -3 -m rdna3_optimization_layer detect
```

4. Print the environment that would be injected:

```powershell
py -3 -m rdna3_optimization_layer env
```

5. Dry-run a launch:

```powershell
py -3 -m rdna3_optimization_layer launch --dry-run -- py -3 -m rdna3_optimization_layer.demo_app
```

6. Launch an application through the layer:

```powershell
py -3 -m rdna3_optimization_layer launch -- py -3 -m rdna3_optimization_layer.demo_app
```

Example with a real program:

```powershell
py -3 -m rdna3_optimization_layer launch -- .\my_app.exe --batch-size 64
```

## How To Integrate It

1. Run your application through `rdna3_optimization_layer launch`.
2. Read `RDNA3_ATLAS_*` environment variables inside your application or wrapper.
3. Optionally parse `RDNA3_ATLAS_POLICY_FILE` to consume the full JSON policy.
4. Use the atlas hints to select block sizes, tiles, vectorization, and memory access patterns.

## Notes

- Exact tuning is based on the RX 7900 XTX reference atlas.
- Other RDNA3 devices are supported by autodetect plus conservative scaling.
- Non-RDNA3 devices are detected and left untouched.
