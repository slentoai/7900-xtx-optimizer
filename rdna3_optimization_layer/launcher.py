from __future__ import annotations

import json
import os
import subprocess
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .policy import RuntimePolicy


def materialize_policy(policy: RuntimePolicy) -> Path:
    payload: dict[str, Any] = {
        "name": policy.name,
        "supported": policy.supported,
        "notes": policy.notes,
        "env": policy.env,
        "atlas_overrides": policy.atlas_overrides,
    }
    path = Path(tempfile.gettempdir()) / "rdna3_atlas_policy.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def launch(command: list[str], policy: RuntimePolicy, dry_run: bool = False) -> int:
    env = os.environ.copy()
    env.update(policy.env)
    policy_path = materialize_policy(policy)
    env["RDNA3_ATLAS_POLICY_FILE"] = str(policy_path)

    if dry_run:
        print("Command:", " ".join(command))
        print("Policy file:", policy_path)
        print("Injected environment:")
        for key in sorted(policy.env):
            print(f"  {key}={policy.env[key]}")
        return 0

    completed = subprocess.run(command, env=env, check=False)
    return int(completed.returncode)
