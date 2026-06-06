"""Stats Card SVG template (not used in minimal mode, kept for compatibility)."""

from ..utils import resolve_theme, format_number, esc, METRIC_ICONS, METRIC_LABELS, METRIC_COLORS


def generate(config: dict, stats: dict) -> str:
    theme = resolve_theme(config.get("theme", {}))
    metrics = config.get("stats", {}).get("metrics", ["commits", "stars", "prs", "issues", "repos"])

    width, height = 860, 120
    item_w = width / max(len(metrics), 1)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="{theme["void"]}" rx="12"/>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" fill="none" stroke="{theme["synapse_cyan"]}" stroke-width="1" stroke-opacity="0.25" rx="12"/>',
    ]

    for i, metric in enumerate(metrics):
        x = i * item_w + item_w / 2
        color = theme.get(METRIC_COLORS.get(metric, "synapse_cyan"), theme["synapse_cyan"])
        value = format_number(stats.get(metric, 0))
        label = METRIC_LABELS.get(metric, metric.title())
        icon = METRIC_ICONS.get(metric, "")

        icon_x = x - 8
        parts.append(
            f'<g transform="translate({icon_x:.1f}, 22)" fill="{color}" opacity="0.8">'
            f'<svg width="16" height="16" viewBox="0 0 16 16">{icon}</svg>'
            f'</g>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="58" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" '
            f'font-size="22" font-weight="700" fill="{color}">{esc(value)}</text>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="80" text-anchor="middle" font-family="\'JetBrains Mono\', monospace" '
            f'font-size="11" fill="{theme["text_faint"]}" letter-spacing="1">{esc(label.upper())}</text>'
        )

        if i < len(metrics) - 1:
            sep_x = (i + 1) * item_w
            parts.append(
                f'<line x1="{sep_x:.1f}" y1="20" x2="{sep_x:.1f}" y2="{height-20}" '
                f'stroke="{theme["synapse_cyan"]}" stroke-width="1" stroke-opacity="0.15"/>'
            )

    parts.append("</svg>")
    return "\n".join(parts)
