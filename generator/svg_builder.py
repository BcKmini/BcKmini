"""SVG Builder — orchestrator connecting config, stats, and templates."""

from generator.templates import galaxy_header, stats_card, tech_stack, projects_constellation


class SVGBuilder:
    def __init__(self, config: dict, stats: dict, languages: dict):
        self.config = config
        self.stats = stats
        self.languages = languages

    def render_galaxy_header(self) -> str:
        return galaxy_header.generate(config=self.config, stats=self.stats)

    def render_stats_card(self) -> str:
        return stats_card.generate(config=self.config, stats=self.stats)

    def render_tech_stack(self) -> str:
        return tech_stack.generate(config=self.config, languages=self.languages)

    def render_projects_constellation(self) -> str:
        return projects_constellation.generate(config=self.config, repos=self.config.get("projects", []))
