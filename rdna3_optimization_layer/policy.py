from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .atlas_loader import AtlasBundle
from .gpu_detect import GPUInfo


@dataclass(frozen=True)
class RuntimePolicy:
    name: str
    supported: bool
    notes: list[str]
    env: dict[str, str]
    atlas_overrides: dict[str, Any]


def _scale(value: int, source_cu: int, target_cu: int | None) -> int:
    if not target_cu or target_cu <= 0 or source_cu <= 0:
        return value
    return max(1, round(value * (target_cu / source_cu)))


def build_policy(bundle: AtlasBundle, gpu: GPUInfo) -> RuntimePolicy:
    source_gpu = bundle.profile.get("gpu", {})
    source_cu = int(source_gpu.get("compute_units", 96))
    target_cu = gpu.compute_units or source_cu

    block = bundle.profile.get("block_size", {})
    compute = bundle.profile.get("compute", {})
    lds = bundle.profile.get("lds", {})
    hints = bundle.profile.get("optimization_hints", {})

    atlas_overrides = {
        "target_name": gpu.name,
        "target_arch": gpu.arch,
        "family": gpu.family,
        "recommended_block_size": int(block.get("optimal_block_size", 128)),
        "preferred_block_sizes": block.get("preferred_block_sizes", [128, 256, 32]),
        "wave_size": gpu.wave_size or int(source_gpu.get("wave_size", 32)),
        "recommended_vectorization": hints.get("preferred_vectorization", "float4"),
        "avoid_lds_strides": lds.get("worst_strides", [32]),
        "preferred_lds_strides": lds.get("best_strides", [1, 2, 21, 22, 23]),
        "compute_fp32_optimal_block_size": int(compute.get("fp32", {}).get("optimal_block_size", 512)),
        "compute_fp16_optimal_block_size": int(compute.get("fp16", {}).get("optimal_block_size", 1024)),
        "reduction_items_per_thread": int(compute.get("reduction", {}).get("optimal_items_per_thread", 7)),
        "tile_m": int(compute.get("tiled_gemm", {}).get("optimal_tile_m", 128)),
        "tile_n": int(compute.get("tiled_gemm", {}).get("optimal_tile_n", 128)),
        "waves_per_cu": int(compute.get("wave_scheduling", {}).get("optimal_waves_per_cu", 31)),
        "atomic_unique_targets": _scale(int(compute.get("atomic", {}).get("optimal_unique_targets", 982)), source_cu, target_cu),
        "overlap_working_set_kb": _scale(int(compute.get("overlap", {}).get("optimal_working_set_kb", 82719)), source_cu, target_cu),
    }

    env = {
        # Conservative runtime knobs that can be injected before an app starts.
        "HSA_ENABLE_SDMA": "1",
        "HSA_NO_SCRATCH_RECLAIM": "1",
        "GPU_MAX_HW_QUEUES": str(max(4, min(16, round(target_cu / 8)))),
        # App-visible atlas hints for frameworks or wrappers that choose to honor them.
        "RDNA3_ATLAS_TARGET": gpu.name,
        "RDNA3_ATLAS_ARCH": gpu.arch,
        "RDNA3_ATLAS_BLOCK_SIZE": str(atlas_overrides["recommended_block_size"]),
        "RDNA3_ATLAS_VECTOR_WIDTH": str(atlas_overrides["recommended_vectorization"]),
        "RDNA3_ATLAS_WAVE_SIZE": str(atlas_overrides["wave_size"]),
        "RDNA3_ATLAS_TILE_M": str(atlas_overrides["tile_m"]),
        "RDNA3_ATLAS_TILE_N": str(atlas_overrides["tile_n"]),
        "RDNA3_ATLAS_WAVES_PER_CU": str(atlas_overrides["waves_per_cu"]),
    }

    notes = [
        f"Reference atlas: {bundle.gpu_name} ({bundle.arch})",
        f"Detected target: {gpu.name} ({gpu.arch}) via {gpu.source}",
        "Policy injects conservative driver/runtime environment variables before launch.",
        "Atlas-derived hints are also exported for frameworks or launch wrappers to consume.",
    ]

    supported = gpu.is_rdna3
    if supported and gpu.arch != bundle.arch:
        notes.append("Applying scaled policy because the detected GPU is RDNA3 but not the exact 7900 XTX reference card.")
    if not supported:
        notes.append("Detected GPU is not RDNA3; launch can still proceed, but atlas tuning is disabled.")
        env = {}
        atlas_overrides = {}

    return RuntimePolicy(
        name="rdna3-driver-routing-demo",
        supported=supported,
        notes=notes,
        env=env,
        atlas_overrides=atlas_overrides,
    )
