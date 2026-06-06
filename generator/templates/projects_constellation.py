"""Projects Constellation SVG template (not used in minimal mode, kept for compatibility)."""

from ..utils import resolve_theme, esc, deterministic_random


def generate(config: dict, repos: list = None) -> str:
    theme = resolve_theme(config.get("theme", {}))
    repos = repos or []
    width, height = 860, 300

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="{theme["void"]}" rx="12"/>',
    ]

    if not repos:
        parts += [
            f'<text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" '
            f'font-family="\'JetBrains Mono\', monospace" font-size="13" fill="{theme["text_dim"]}">No pinned repos configured.</text>',
        ]

    parts.append("</svg>")
    return "\n".join(parts)
