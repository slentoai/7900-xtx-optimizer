from __future__ import annotations

import json
import os
from pathlib import Path


def main() -> int:
    policy_path = os.environ.get("RDNA3_ATLAS_POLICY_FILE")
    print("RDNA3 optimization layer demo")
    print("Detected injected values:")
    for key in sorted(k for k in os.environ if k.startswith("RDNA3_ATLAS_") or k in {"GPU_MAX_HW_QUEUES", "HSA_ENABLE_SDMA", "HSA_NO_SCRATCH_RECLAIM"}):
        print(f"  {key}={os.environ[key]}")

    if policy_path and Path(policy_path).exists():
        payload = json.loads(Path(policy_path).read_text(encoding="utf-8"))
        print("\nPolicy summary:")
        print(f"  supported={payload.get('supported')}")
        for note in payload.get("notes", []):
            print(f"  note: {note}")
    else:
        print("\nNo policy file was provided.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
