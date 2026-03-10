from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AtlasBundle:
    root: Path
    profile: dict[str, Any]
    guide: dict[str, Any]

    @property
    def gpu_name(self) -> str:
        gpu = self.profile.get("gpu", {})
        if isinstance(gpu, dict):
            return str(gpu.get("name", "RX 7900 XTX"))
        return str(self.guide.get("gpu", "RX 7900 XTX"))

    @property
    def arch(self) -> str:
        gpu = self.profile.get("gpu", {})
        if isinstance(gpu, dict):
            return str(gpu.get("arch", "gfx1100"))
        return "gfx1100"


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_atlas_bundle(root: Path | None = None) -> AtlasBundle:
    base = root or Path(__file__).resolve().parent.parent
    profile = _read_json(base / "gfx1100_atlas_profile.json")
    guide = _read_json(base / "rdna3_optimization_guide.json")
    return AtlasBundle(root=base, profile=profile, guide=guide)
