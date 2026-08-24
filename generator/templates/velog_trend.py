"""Velog daily total-views trend chart (area + line), built from the local
JSON snapshot history — no charting library, same hand-rolled SVG approach
as the rest of this generator.
"""

from generator.utils import resolve_theme, format_number, esc

LIGHT_OVERRIDES = {
    "void": "#ffffff",
    "text_bright": "#1f2328",
    "text_faint": "#6e7781",
}


def generate(config: dict, history: list, key: str = "total_views", days: int = 30) -> str:
    theme = resolve_theme(config.get("theme", {}))
    width, height = 860, 220
    pad_l, pad_r, pad_t, pad_b = 50, 24, 40, 36

    points = history[-days:]

    style = f"""<style>
      .bg {{ fill: {theme['void']}; }}
      .border {{ stroke: {theme['synapse_cyan']}; }}
      .title {{ fill: {theme['text_bright']}; }}
      .sub {{ fill: {theme['text_faint']}; }}
      .axis {{ fill: {theme['text_faint']}; }}
      @media (prefers-color-scheme: light) {{
        .bg {{ fill: {LIGHT_OVERRIDES['void']}; }}
        .title {{ fill: {LIGHT_OVERRIDES['text_bright']}; }}
        .sub {{ fill: {LIGHT_OVERRIDES['text_faint']}; }}
        .axis {{ fill: {LIGHT_OVERRIDES['text_faint']}; }}
      }}
    </style>"""

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        style,
        f'<rect class="bg" width="{width}" height="{height}" rx="12"/>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" fill="none" class="border" stroke-width="1" stroke-opacity="0.25" rx="12"/>',
        f'<text x="24" y="30" class="title" font-family="\'JetBrains Mono\', monospace" font-size="14" font-weight="700">Total Views — Last {days}d</text>',
    ]

    if len(points) == 0:
        parts.append(
            f'<text x="{width/2}" y="{height/2}" text-anchor="middle" class="sub" '
            f'font-family="\'JetBrains Mono\', monospace" font-size="12">아직 수집된 데이터가 없습니다.</text>'
        )
        parts.append("</svg>")
        return "\n".join(parts)

    if len(points) == 1:
        parts.append(
            f'<text x="{width/2}" y="{height/2 - 6}" text-anchor="middle" class="title" '
            f'font-family="\'JetBrains Mono\', monospace" font-size="26" font-weight="700">{format_number(points[0].get(key, 0))}</text>'
        )
        parts.append(
            f'<text x="{width/2}" y="{height/2 + 16}" text-anchor="middle" class="sub" '
            f'font-family="\'JetBrains Mono\', monospace" font-size="11">{esc(points[0]["date"])} · 데이터가 더 쌍이면 추이가 표시됩니다</text>'
        )
        parts.append("</svg>")
        return "\n".join(parts)

    values = [p.get(key, 0) for p in points]
    v_min, v_max = min(values), max(values)
    if v_min == v_max:
        v_min -= 1
        v_max += 1

    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    n = len(points)

    def px(i):
        return pad_l + (i / (n - 1)) * plot_w

    def py(v):
        return pad_t + plot_h - ((v - v_min) / (v_max - v_min)) * plot_h

    coords = [(px(i), py(v)) for i, v in enumerate(values)]
    line_path = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in coords)
    area_path = line_path + f" L {coords[-1][0]:.1f} {pad_t+plot_h:.1f} L {coords[0][0]:.1f} {pad_t+plot_h:.1f} Z"

    parts.append(f'<path d="{area_path}" fill="{theme["synapse_cyan"]}" opacity="0.12"/>')
    parts.append(f'<path d="{line_path}" fill="none" stroke="{theme["synapse_cyan"]}" stroke-width="2"/>')
    parts.append(f'<circle cx="{coords[-1][0]:.1f}" cy="{coords[-1][1]:.1f}" r="4" fill="{theme["synapse_cyan"]}"/>')

    parts.append(
        f'<text x="{pad_l}" y="{height-12}" class="axis" font-family="\'JetBrains Mono\', monospace" '
        f'font-size="10">{esc(points[0]["date"])}</text>'
    )
    parts.append(
        f'<text x="{width-pad_r}" y="{height-12}" text-anchor="end" class="axis" '
        f'font-family="\'JetBrains Mono\', monospace" font-size="10">{esc(points[-1]["date"])}</text>'
    )
    parts.append(
        f'<text x="{width-pad_r}" y="{pad_t+2}" text-anchor="end" class="sub" '
        f'font-family="\'JetBrains Mono\', monospace" font-size="11">{format_number(values[-1])}</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts)
