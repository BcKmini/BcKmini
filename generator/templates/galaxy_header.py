"""Galaxy Header SVG template (not used in minimal mode, kept for compatibility)."""

from ..utils import resolve_theme, esc, deterministic_random


def generate(config: dict, stats: dict = None) -> str:
    theme = resolve_theme(config.get("theme", {}))
    profile = config.get("profile", {})
    name = profile.get("name", config.get("username", "Developer"))
    tagline = profile.get("tagline", "")

    width, height = 860, 200
    stars = _stars(width, height, theme)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="hdrGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{theme['void']}"/>
      <stop offset="100%" stop-color="{theme['nebula']}"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#hdrGrad)" rx="12"/>
  {stars}
  <text x="50%" y="90" text-anchor="middle" font-family="'JetBrains Mono', monospace"
        font-size="36" font-weight="700" fill="{theme['text_bright']}">{esc(name)}</text>
  <text x="50%" y="130" text-anchor="middle" font-family="'JetBrains Mono', monospace"
        font-size="16" fill="{theme['synapse_cyan']}" opacity="0.9">{esc(tagline)}</text>
</svg>"""


def _stars(width: int, height: int, theme: dict) -> str:
    xs = deterministic_random("hdr_sx", 30, 0, width)
    ys = deterministic_random("hdr_sy", 30, 0, height)
    szs = deterministic_random("hdr_ss", 30, 0.4, 1.8)
    ops = deterministic_random("hdr_so", 30, 0.15, 0.7)
    parts = []
    for i in range(30):
        parts.append(f'<circle cx="{xs[i]:.1f}" cy="{ys[i]:.1f}" r="{szs[i]:.1f}" fill="{theme["text_bright"]}" opacity="{ops[i]:.2f}"/>')
    return "\n  ".join(parts)
