"""Velog recent-posts card (latest N posts by release date)."""

from generator.utils import resolve_theme, format_number, esc, wrap_text

LIGHT_OVERRIDES = {
    "void": "#ffffff",
    "text_bright": "#1f2328",
    "text_faint": "#6e7781",
}

ROW_H = 40
HEADER_H = 60
PAD = 24


def generate(config: dict, posts: list) -> str:
    theme = resolve_theme(config.get("theme", {}))
    width = 860
    rows = posts[:5]
    height = HEADER_H + max(len(rows), 1) * ROW_H + 16

    style = f"""<style>
      .bg {{ fill: {theme['void']}; }}
      .border {{ stroke: {theme['synapse_cyan']}; }}
      .title {{ fill: {theme['text_bright']}; }}
      .sub {{ fill: {theme['text_faint']}; }}
      .row-title {{ fill: {theme['text_bright']}; }}
      .row-meta {{ fill: {theme['text_faint']}; }}
      @media (prefers-color-scheme: light) {{
        .bg {{ fill: {LIGHT_OVERRIDES['void']}; }}
        .title {{ fill: {LIGHT_OVERRIDES['text_bright']}; }}
        .sub {{ fill: {LIGHT_OVERRIDES['text_faint']}; }}
        .row-title {{ fill: {LIGHT_OVERRIDES['text_bright']}; }}
        .row-meta {{ fill: {LIGHT_OVERRIDES['text_faint']}; }}
      }}
    </style>"""

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        style,
        f'<rect class="bg" width="{width}" height="{height}" rx="12"/>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" fill="none" class="border" stroke-width="1" stroke-opacity="0.25" rx="12"/>',
        f'<text x="{PAD}" y="34" class="title" font-family="\'JetBrains Mono\', monospace" font-size="15" font-weight="700">Recent Posts</text>',
        f'<line x1="0" y1="{HEADER_H-14}" x2="{width}" y2="{HEADER_H-14}" class="border" stroke-width="1" stroke-opacity="0.15"/>',
    ]

    if not rows:
        parts.append(
            f'<text x="{width/2}" y="{HEADER_H+20}" text-anchor="middle" class="sub" '
            f'font-family="\'JetBrains Mono\', monospace" font-size="12">데이터가 아직 없습니다.</text>'
        )
    else:
        for i, post in enumerate(rows):
            y = HEADER_H + i * ROW_H
            mid_y = y + ROW_H / 2
            titles = wrap_text(post["title"], 46)
            title = titles[0] if titles else "(제목 없음)"
            date = (post.get("released_at") or "")[:10]

            parts.append(
                f'<text x="{PAD}" y="{mid_y+4:.1f}" class="sub" font-family="\'JetBrains Mono\', monospace" '
                f'font-size="11">{esc(date)}</text>'
            )
            parts.append(
                f'<text x="{PAD+96}" y="{mid_y+4:.1f}" class="row-title" font-family="\'JetBrains Mono\', monospace" '
                f'font-size="12">{esc(title)}</text>'
            )
            parts.append(
                f'<text x="{width-PAD}" y="{mid_y+4:.1f}" text-anchor="end" class="row-meta" '
                f'font-family="\'JetBrains Mono\', monospace" font-size="11">'
                f'{format_number(post["views"])} views · {format_number(post["likes"])}♥</text>'
            )

    parts.append("</svg>")
    return "\n".join(parts)
