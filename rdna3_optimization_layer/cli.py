from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .atlas_loader import load_atlas_bundle
from .gpu_detect import detect_gpu
from .launcher import launch
from .policy import build_policy


def _build_runtime_policy():
    bundle = load_atlas_bundle()
    gpu = detect_gpu()
    return bundle, gpu, build_policy(bundle, gpu)


def cmd_detect(_: argparse.Namespace) -> int:
    _, gpu, policy = _build_runtime_policy()
    print(json.dumps({"gpu": asdict(gpu), "supported": policy.supported, "notes": policy.notes}, indent=2))
    return 0


def cmd_env(_: argparse.Namespace) -> int:
    _, _, policy = _build_runtime_policy()
    print(json.dumps({"env": policy.env, "atlas_overrides": policy.atlas_overrides, "notes": policy.notes}, indent=2))
    return 0


def cmd_launch(args: argparse.Namespace) -> int:
    _, _, policy = _build_runtime_policy()
    return launch(args.command, policy, dry_run=args.dry_run)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RDNA3 optimization layer demo by Craig Hasselbring")
    subparsers = parser.add_subparsers(dest="command_name", required=True)

    detect_parser = subparsers.add_parser("detect", help="Detect the current GPU and evaluate support")
    detect_parser.set_defaults(func=cmd_detect)

    env_parser = subparsers.add_parser("env", help="Print the environment variables that would be injected")
    env_parser.set_defaults(func=cmd_env)

    launch_parser = subparsers.add_parser("launch", help="Launch an application through the optimization layer")
    launch_parser.add_argument("--dry-run", action="store_true", help="Print the injected environment without launching")
    launch_parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to run after '--'")
    launch_parser.set_defaults(func=cmd_launch)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command_name == "launch":
        if args.command and args.command[0] == "--":
            args.command = args.command[1:]
        if not args.command:
            parser.error("launch requires a command after '--'")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
