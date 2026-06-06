"""Interactive setup wizard for initializing galaxy-profile config."""

from __future__ import annotations

import re
import sys

import yaml

from .tech_catalog import TECH_CATALOG

DEFAULT_ARMS = [
    {"name": "Languages", "color": "synapse_cyan", "items": []},
    {"name": "Frameworks", "color": "dendrite_violet", "items": []},
    {"name": "DevOps", "color": "axon_amber", "items": []},
]

COLORS = ["synapse_cyan", "dendrite_violet", "axon_amber"]


def prompt(question: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        value = input(f"{question}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    return value or default


def prompt_list(question: str, hint: str = "") -> list[str]:
    print(f"{question}")
    if hint:
        print(f"  ({hint})")
    try:
        raw = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def show_categories():
    print("\n  Available tech categories:")
    for cat, items in TECH_CATALOG.items():
        print(f"    [{cat}]: {', '.join(items[:5])}...")


def prompt_galaxy_arms() -> list[dict]:
    print("\n--- Galaxy Arms (Technology Sectors) ---")
    print("Define 1-5 technology sectors that represent your expertise.")
    show_categories()

    arms = []
    arm_index = 0
    while arm_index < 5:
        if arm_index > 0:
            try:
                cont = input(f"\nAdd another sector? (y/n) [n]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if cont != "y":
                break

        print(f"\nSector {arm_index + 1}:")
        name = prompt("  Sector name (e.g., 'AI & ML', 'Web Dev')")
        if not name:
            if arm_index == 0:
                print("  Using defaults...")
                return DEFAULT_ARMS
            break

        color = COLORS[arm_index % len(COLORS)]
        print(f"  Color: {color} (auto-assigned)")

        items = prompt_list(
            "  Technologies (comma-separated)",
            "e.g., Python, TensorFlow, FastAPI"
        )

        arms.append({"name": name, "color": color, "items": items})
        arm_index += 1

    return arms if arms else DEFAULT_ARMS


def prompt_exclude_languages() -> list[str]:
    print("\nLanguages to exclude from Language Telemetry (markup/config/noise):")
    defaults = "HTML, CSS, Shell, Makefile"
    raw = prompt(f"  Exclude (comma-separated)", defaults)
    return [item.strip() for item in raw.split(",") if item.strip()]


def run_wizard(output_path: str = "config.yml"):
    print("=" * 60)
    print("  Galaxy Profile Setup Wizard")
    print("=" * 60)

    print("\n--- Basic Information ---")
    username = prompt("GitHub username")
    name = prompt("Display name", username)
    tagline = prompt("Tagline", "Software Engineer")
    location = prompt("Location", "")
    bio = prompt("Short bio (one line)", "")
    philosophy = prompt("Philosophy / motto", "")
    email = prompt("Email (optional)", "")

    arms = prompt_galaxy_arms()
    exclude_langs = prompt_exclude_languages()

    print("\n--- Stats Metrics ---")
    print("  Which metrics to show? [commits, stars, prs, issues, repos]")
    raw_metrics = prompt("  Metrics (comma-separated)", "commits, stars, prs, issues, repos")
    metrics = [m.strip() for m in raw_metrics.split(",") if m.strip()]

    config = {
        "username": username,
        "profile": {
            "name": name,
            "tagline": tagline,
            **({"location": location} if location else {}),
            **({"bio": bio} if bio else {}),
            **({"philosophy": philosophy} if philosophy else {}),
        },
        **({"social": {"email": email}} if email else {}),
        "galaxy_arms": arms,
        "theme": {
            "void": "#080c14",
            "nebula": "#0f1623",
            "star_dust": "#1a2332",
            "synapse_cyan": "#00d4ff",
            "dendrite_violet": "#a78bfa",
            "axon_amber": "#ffb020",
            "text_bright": "#f1f5f9",
            "text_dim": "#94a3b8",
            "text_faint": "#64748b",
        },
        "stats": {"metrics": metrics},
        "languages": {
            "exclude": exclude_langs,
            "max_display": 8,
        },
    }

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"\n✓ Config written to {output_path}")
        print("  Review and edit it, then run: python -m generator.main generate")
    except OSError as e:
        print(f"\n✗ Could not write config: {e}", file=sys.stderr)
        sys.exit(1)
