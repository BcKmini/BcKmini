"""Tech Stack SVG template — Language Telemetry + Focus Sectors radar."""

from __future__ import annotations

import math
from ..utils import (
    resolve_theme, resolve_arm_colors, calculate_language_percentages,
    format_number, esc, svg_arc_path, deterministic_random,
)


def generate(config: dict, languages: dict) -> str:
    theme = resolve_theme(config.get("theme", {}))
    lang_cfg = config.get("languages", {})
    exclude = lang_cfg.get("exclude", ["HTML", "CSS", "Shell", "Makefile"])
    max_display = lang_cfg.get("max_display", 8)
    galaxy_arms = config.get("galaxy_arms", [])

    lang_data = calculate_language_percentages(languages, exclude, max_display)
    arm_colors = resolve_arm_colors(galaxy_arms, theme)

    width = 960
    height = 520
    pad = 40
    left_w = 370
    right_w = width - left_w - pad * 3

    stars_svg = _generate_stars(width, height, theme)
    lang_svg = _language_telemetry(lang_data, left_w, height - pad * 2, theme, pad)
    radar_svg = _focus_sectors_radar(galaxy_arms, arm_colors, right_w, height - pad * 2, theme)

    radar_x = left_w + pad * 2

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&amp;display=swap');
      .mono {{ font-family: 'JetBrains Mono', 'Courier New', monospace; }}
    </style>
    {_defs(theme)}
  </defs>
  <!-- Background -->
  <rect width="{width}" height="{height}" fill="{theme['void']}" rx="16"/>
  <rect width="{width}" height="{height}" fill="url(#bgGrad)" rx="16"/>
  {stars_svg}
  <!-- Border -->
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="none" stroke="{theme['synapse_cyan']}" stroke-width="1" stroke-opacity="0.3" rx="16"/>
  <!-- Divider -->
  <line x1="{left_w + pad}" y1="{pad}" x2="{left_w + pad}" y2="{height - pad}" stroke="{theme['synapse_cyan']}" stroke-width="1" stroke-opacity="0.2"/>
  <!-- Left panel: Language Telemetry -->
  <g transform="translate({pad}, {pad})">
    {lang_svg}
  </g>
  <!-- Right panel: Focus Sectors -->
  <g transform="translate({radar_x}, {pad})">
    {radar_svg}
  </g>
</svg>"""


def _defs(theme: dict) -> str:
    return f"""
    <radialGradient id="bgGrad" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="{theme['nebula']}" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="{theme['void']}" stop-opacity="0"/>
    </radialGradient>"""


def _generate_stars(width: int, height: int, theme: dict) -> str:
    xs = deterministic_random("star_x", 40, 0, width)
    ys = deterministic_random("star_y", 40, 0, height)
    sizes = deterministic_random("star_s", 40, 0.5, 2.0)
    opacities = deterministic_random("star_o", 40, 0.2, 0.8)
    parts = []
    for i in range(40):
        dur = 2 + (i % 5)
        parts.append(
            f'<circle cx="{xs[i]:.1f}" cy="{ys[i]:.1f}" r="{sizes[i]:.1f}" fill="{theme["text_bright"]}" opacity="{opacities[i]:.2f}">'
            f'<animate attributeName="opacity" values="{opacities[i]:.2f};{max(0.05, opacities[i]-0.4):.2f};{opacities[i]:.2f}" dur="{dur}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    return "\n  ".join(parts)


def _section_title(text: str, x: float, y: float, theme: dict, accent_color: str = None) -> str:
    color = accent_color or theme["synapse_cyan"]
    return (
        f'<text x="{x}" y="{y}" class="mono" font-size="11" font-weight="600" '
        f'fill="{color}" letter-spacing="2" opacity="0.9">{esc(text)}</text>'
        f'<line x1="{x}" y1="{y+6}" x2="{x+160}" y2="{y+6}" stroke="{color}" stroke-width="1" stroke-opacity="0.4"/>'
    )


def _language_telemetry(lang_data: list, panel_w: float, panel_h: float, theme: dict, pad: float) -> str:
    parts = [_section_title("LANGUAGE TELEMETRY", 0, 0, theme)]
    if not lang_data:
        parts.append(f'<text x="0" y="40" class="mono" font-size="11" fill="{theme["text_dim"]}">No language data available.</text>')
        return "\n".join(parts)

    bar_area_w = panel_w - 20
    bar_h = 7
    spacing = (panel_h - 30) / max(len(lang_data), 1)
    spacing = min(spacing, 44)

    for i, lang in enumerate(lang_data):
        y_base = 28 + i * spacing
        pct = lang["percentage"]
        bar_w = max(2.0, (pct / 100) * bar_area_w)
        color = lang["color"]

        parts.append(
            f'<text x="0" y="{y_base}" class="mono" font-size="11" fill="{theme["text_dim"]}">{esc(lang["name"])}</text>'
            f'<text x="{bar_area_w}" y="{y_base}" class="mono" font-size="10" fill="{theme["text_faint"]}" text-anchor="end">{pct}%</text>'
        )
        y_bar = y_base + 4
        parts.append(
            f'<rect x="0" y="{y_bar}" width="{bar_area_w}" height="{bar_h}" fill="{theme["star_dust"]}" rx="3"/>'
            f'<rect x="0" y="{y_bar}" width="0" height="{bar_h}" fill="{color}" rx="3" opacity="0.9">'
            f'<animate attributeName="width" from="0" to="{bar_w:.1f}" dur="1.{i}s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>'
            f'</rect>'
        )

    return "\n".join(parts)


def _focus_sectors_radar(galaxy_arms: list, arm_colors: list, panel_w: float, panel_h: float, theme: dict) -> str:
    if not galaxy_arms:
        return f'<text x="0" y="20" class="mono" font-size="11" fill="{theme["text_dim"]}">No sectors configured.</text>'

    parts = [_section_title("FOCUS SECTORS", 0, 0, theme)]

    cx = panel_w / 2
    cy = (panel_h - 20) / 2 + 20
    radar_r = 145  # fixed: prevents labels overflowing 470px-wide panel

    n = len(galaxy_arms)
    rings = 4

    # Grid rings
    for ring in range(1, rings + 1):
        r = radar_r * ring / rings
        opacity = 0.08 + ring * 0.04
        pts = []
        for i in range(n):
            angle = math.radians(-90 + i * 360 / n)
            pts.append(f"{cx + r * math.cos(angle):.1f},{cy + r * math.sin(angle):.1f}")
        parts.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{theme["synapse_cyan"]}" stroke-width="1" stroke-opacity="{opacity:.2f}"/>')

    # Axis lines
    for i in range(n):
        angle = math.radians(-90 + i * 360 / n)
        x2 = cx + radar_r * math.cos(angle)
        y2 = cy + radar_r * math.sin(angle)
        parts.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{theme["synapse_cyan"]}" stroke-width="1" stroke-opacity="0.15"/>')

    # Value scores (based on item count, normalized)
    max_items = max((len(arm.get("items", [])) for arm in galaxy_arms), default=1)
    scores = [min(1.0, len(arm.get("items", [])) / max(max_items, 5)) * 0.75 + 0.25 for arm in galaxy_arms]

    # Filled area (animated)
    def make_points(scale=1.0):
        pts = []
        for i, score in enumerate(scores):
            angle = math.radians(-90 + i * 360 / n)
            r = radar_r * score * scale
            pts.append(f"{cx + r * math.cos(angle):.1f},{cy + r * math.sin(angle):.1f}")
        return " ".join(pts)

    fill_color = theme.get("synapse_cyan", "#00d4ff")
    parts.append(
        f'<polygon points="{make_points(0.01)}" fill="{fill_color}" fill-opacity="0.08" stroke="{fill_color}" stroke-width="2" stroke-opacity="0.7">'
        f'<animate attributeName="points" from="{make_points(0.01)}" to="{make_points(1.0)}" dur="1.4s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>'
        f'</polygon>'
    )

    # Dot on each axis vertex
    for i, (arm, color, score) in enumerate(zip(galaxy_arms, arm_colors, scores)):
        angle = math.radians(-90 + i * 360 / n)
        r = radar_r * score
        vx = cx + r * math.cos(angle)
        vy = cy + r * math.sin(angle)
        parts.append(
            f'<circle cx="{vx:.1f}" cy="{vy:.1f}" r="4" fill="{color}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="1.2s" dur="0.3s" fill="freeze"/>'
            f'</circle>'
        )

    # Labels
    label_r = radar_r + 22
    for i, (arm, color) in enumerate(zip(galaxy_arms, arm_colors)):
        angle = math.radians(-90 + i * 360 / n)
        lx = cx + label_r * math.cos(angle)
        ly = cy + label_r * math.sin(angle)
        anchor = "middle"
        if lx < cx - 10:
            anchor = "end"
        elif lx > cx + 10:
            anchor = "start"
        dy_offset = 0
        if ly < cy - 5:
            dy_offset = -6
        elif ly > cy + 5:
            dy_offset = 14
        parts.append(
            f'<text x="{lx:.1f}" y="{ly + dy_offset:.1f}" class="mono" font-size="10" font-weight="600" '
            f'fill="{color}" text-anchor="{anchor}" opacity="0.9">{esc(arm["name"])}</text>'
        )
        if arm.get("items"):
            n_items = 3 if anchor == "middle" else 2
            items_str = " · ".join(arm["items"][:n_items])
            parts.append(
                f'<text x="{lx:.1f}" y="{ly + dy_offset + 13:.1f}" class="mono" font-size="9" '
                f'fill="{theme["text_faint"]}" text-anchor="{anchor}" opacity="0.7">{esc(items_str)}</text>'
            )

    return "\n".join(parts)
