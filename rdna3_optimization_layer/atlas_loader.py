from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
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


def _read_packaged_json(name: str) -> dict[str, Any]:
    resource = resources.files("rdna3_optimization_layer").joinpath("data", name)
    with resource.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_atlas_bundle(root: Path | None = None) -> AtlasBundle:
    if root is not None:
        base = root
        profile = _read_json(base / "gfx1100_atlas_profile.json")
        guide = _read_json(base / "rdna3_optimization_guide.json")
        return AtlasBundle(root=base, profile=profile, guide=guide)

    base = Path(__file__).resolve().parent
    profile = _read_packaged_json("gfx1100_atlas_profile.json")
    guide = _read_packaged_json("rdna3_optimization_guide.json")
    return AtlasBundle(root=base, profile=profile, guide=guide)
