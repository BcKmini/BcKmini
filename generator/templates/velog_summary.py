"""Velog summary card — total views/likes/posts with a 7-day delta.

Supports light/dark automatically via `prefers-color-scheme`, since this
card (unlike the GitHub-stats ones) is meant to also read well for viewers
without a synced dark theme.
"""

from generator.utils import resolve_theme, format_number, esc

LIGHT_OVERRIDES = {
    "void": "#ffffff",
    "text_bright": "#1f2328",
    "text_faint": "#6e7781",
}

METRICS = [
    ("total_views", "TOTAL VIEWS", "synapse_cyan", "view_diff"),
    ("total_likes", "TOTAL LIKES", "dendrite_violet", "like_diff"),
    ("total_posts", "TOTAL POSTS", "axon_amber", "post_diff"),
]


def _diff_label(value: int) -> str:
    if value > 0:
        return f"▲ {value:,}"
    if value < 0:
        return f"▼ {abs(value):,}"
    return "– 0"


def _diff_class(value: int) -> str:
    if value > 0:
        return "up"
    if value < 0:
        return "down"
    return "flat"


def generate(config: dict, velog: dict) -> str:
    theme = resolve_theme(config.get("theme", {}))
    width, height = 860, 150
    item_w = width / len(METRICS)
    username = velog.get("username", "")

    style = f"""<style>
      .bg {{ fill: {theme['void']}; }}
      .border {{ stroke: {theme['synapse_cyan']}; }}
      .title {{ fill: {theme['text_bright']}; }}
      .sub {{ fill: {theme['text_faint']}; }}
      .up {{ fill: #3fb950; }}
      .down {{ fill: #f85149; }}
      .flat {{ fill: {theme['text_faint']}; }}
      @media (prefers-color-scheme: light) {{
        .bg {{ fill: {LIGHT_OVERRIDES['void']}; }}
        .title {{ fill: {LIGHT_OVERRIDES['text_bright']}; }}
        .sub {{ fill: {LIGHT_OVERRIDES['text_faint']}; }}
      }}
    </style>"""

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        style,
        f'<rect class="bg" width="{width}" height="{height}" rx="12"/>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" fill="none" class="border" stroke-width="1" stroke-opacity="0.25" rx="12"/>',
        f'<text x="24" y="34" class="title" font-family="\'JetBrains Mono\', monospace" font-size="15" font-weight="700">📝 Velog Analytics</text>',
        f'<text x="24" y="52" class="sub" font-family="\'JetBrains Mono\', monospace" font-size="11">@{esc(username)}</text>',
        f'<line x1="0" y1="66" x2="{width}" y2="66" class="border" stroke-width="1" stroke-opacity="0.15"/>',
    ]

    for i, (key, label, color_key, diff_key) in enumerate(METRICS):
        x = i * item_w + item_w / 2
        color = theme.get(color_key, theme["synapse_cyan"])
        value = format_number(velog.get(key, 0))
        diff = velog.get(diff_key, 0)

        parts.append(
            f'<text x="{x:.1f}" y="105" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" '
            f'font-size="30" font-weight="700" fill="{color}">{esc(value)}</text>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="124" text-anchor="middle" class="sub" font-family="\'JetBrains Mono\', monospace" '
            f'font-size="10" letter-spacing="1">{esc(label)}</text>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="140" text-anchor="middle" class="{_diff_class(diff)}" '
            f'font-family="\'JetBrains Mono\', monospace" font-size="11">{esc(_diff_label(diff))} / 7d</text>'
        )
        if i < len(METRICS) - 1:
            sep_x = (i + 1) * item_w
            parts.append(
                f'<line x1="{sep_x:.1f}" y1="76" x2="{sep_x:.1f}" y2="{height-14}" '
                f'class="border" stroke-width="1" stroke-opacity="0.15"/>'
            )

    parts.append("</svg>")
    return "\n".join(parts)
