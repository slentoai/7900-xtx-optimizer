# 7900 XTX Optimizer Release Notes

Maintainer: Craig Hasselbring

## Overview

This repository publishes the open RX 7900 XTX atlas data and a demo RDNA3 optimization layer.
The optimization layer autodetects RDNA3 GPUs, derives a runtime policy from the 7900 XTX atlas,
and routes application launches through an atlas-backed user-space shim.

## Included

- `rx7900xtx_atlas.db`: SQLite atlas database
- `atlas_export.json.gz`: compressed JSON export of the atlas
- `rdna3_optimization_layer/`: autodetect, policy derivation, and launch wrapper demo
- Linux and Windows quick-start documentation
- `setup.py` and `pyproject.toml` for packaging

## Important Note

`atlas_export.json.gz` is compressed to stay within GitHub's file size limits.
Decompress it with one of the following commands if you want the raw JSON export:

Linux/macOS:
```bash
gunzip -k atlas_export.json.gz
```

Windows PowerShell:
```powershell
gzip -d atlas_export.json.gz
```

## Scope

This project does not modify AMD drivers.
It demonstrates a user-space optimization routing layer that injects conservative driver/runtime
settings and exports atlas hints for RDNA3 applications and wrappers.
