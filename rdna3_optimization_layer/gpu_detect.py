from __future__ import annotations

import platform
import re
import subprocess
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class GPUInfo:
    vendor: str
    name: str
    arch: str
    family: str
    compute_units: int | None
    wave_size: int | None
    source: str

    @property
    def is_rdna3(self) -> bool:
        return self.vendor == "AMD" and self.family == "RDNA3"


_RDNA3_SIGNATURES = {
    "gfx1100": {"family": "RDNA3", "compute_units": 96, "wave_size": 32},
    "gfx1101": {"family": "RDNA3", "compute_units": 60, "wave_size": 32},
    "gfx1102": {"family": "RDNA3", "compute_units": 32, "wave_size": 32},
    "gfx1103": {"family": "RDNA3", "compute_units": 12, "wave_size": 32},
}


def _run(command: list[str]) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return ""
    return (result.stdout or "") + (result.stderr or "")


def _first_match(patterns: Iterable[str], text: str) -> str:
    lowered = text.lower()
    for pattern in patterns:
        if pattern.lower() in lowered:
            return pattern
    return ""


def _infer_arch(text: str) -> str:
    lowered = text.lower()
    for arch in _RDNA3_SIGNATURES:
        if arch in lowered:
            return arch
    if "7900 xtx" in lowered:
        return "gfx1100"
    if "7900 xt" in lowered:
        return "gfx1100"
    if "7800 xt" in lowered or "7700 xt" in lowered:
        return "gfx1101"
    if "7600" in lowered:
        return "gfx1102"
    if "radeon 880m" in lowered or "radeon 890m" in lowered:
        return "gfx1103"
    return ""


def _pick_best_name(source: str, text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if source == "lspci":
        display_lines = [
            line for line in lines
            if re.search(r"(VGA compatible controller|Display controller|3D controller)", line, re.I)
        ]
        amd_display_lines = [
            line for line in display_lines
            if re.search(r"(AMD|Radeon|7900|7800|7700|7600|gfx110)", line, re.I)
        ]
        if amd_display_lines:
            return amd_display_lines[0]
    return next(
        (line for line in lines if re.search(r"(AMD|Radeon|7900|7800|7700|7600|gfx110)", line, re.I)),
        "AMD RDNA3 GPU",
    )


def _linux_candidates() -> list[tuple[str, str]]:
    return [
        ("rocm-smi", _run(["rocm-smi", "--showproductname"])),
        ("rocminfo", _run(["rocminfo"])),
        ("lspci", _run(["lspci"])),
    ]


def _windows_candidates() -> list[tuple[str, str]]:
    return [
        (
            "powershell",
            _run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name",
                ]
            ),
        ),
        ("wmic", _run(["wmic", "path", "win32_VideoController", "get", "name"])),
    ]


def detect_gpu() -> GPUInfo:
    system = platform.system()
    candidates = _windows_candidates() if system == "Windows" else _linux_candidates()

    for source, text in candidates:
        if not text.strip():
            continue
        arch = _infer_arch(text)
        amd_hint = _first_match(["amd", "radeon", "7900 xtx", "gfx110"], text)
        if not amd_hint and not arch:
            continue

        name = _pick_best_name(source, text)
        signature = _RDNA3_SIGNATURES.get(arch, {})
        family = str(signature.get("family", "RDNA3" if arch else "Unknown"))
        return GPUInfo(
            vendor="AMD",
            name=name,
            arch=arch or "unknown",
            family=family,
            compute_units=signature.get("compute_units"),
            wave_size=signature.get("wave_size"),
            source=source,
        )

    return GPUInfo(
        vendor="Unknown",
        name="Unknown GPU",
        arch="unknown",
        family="Unknown",
        compute_units=None,
        wave_size=None,
        source="none",
    )
