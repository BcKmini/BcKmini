"""Entry point for the Galaxy Profile README generator."""

import argparse
import logging
import os
import sys

import requests
import yaml

from generator.config import ConfigError, validate_config
from generator.github_api import GitHubAPI
from generator.svg_builder import SVGBuilder

logger = logging.getLogger(__name__)

DEMO_STATS = {"commits": 1847, "stars": 342, "prs": 156, "issues": 89, "repos": 42}
DEMO_LANGUAGES = {
    "Python": 450000,
    "TypeScript": 380000,
    "JavaScript": 120000,
    "Go": 95000,
    "Rust": 45000,
    "Shell": 30000,
    "Dockerfile": 15000,
    "CSS": 10000,
}


def generate_velog_cards(config: dict, builder: SVGBuilder, output_dir: str) -> None:
    """velog.username이 설정되어 있고 토큰이 있으면 velog 통계 SVG 3종을 생성한다."""
    velog_username = (config.get("velog") or {}).get("username")
    if not velog_username:
        return
    if not (os.environ.get("VELOG_ACCESS_TOKEN") and os.environ.get("VELOG_REFRESH_TOKEN")):
        logger.info("VELOG_ACCESS_TOKEN/VELOG_REFRESH_TOKEN이 없어 velog 카드 생성을 건너뜁니다.")
        return

    from generator.velog_api import VelogClient, VelogError
    from generator.velog_history import diff_from_days_ago, update_history

    logger.info("Fetching Velog stats for @%s...", velog_username)
    try:
        client = VelogClient(velog_username)
        velog_stats = client.fetch_user_stats()
    except VelogError as e:
        logger.warning("Velog stats 조회 실패 (%s). 이전 SVG를 유지합니다.", e)
        return

    history_path = os.path.join(os.path.dirname(__file__), "..", "data", "velog_history.json")
    history = update_history(history_path, velog_stats)

    velog_stats["view_diff"] = diff_from_days_ago(history, 7, "total_views")
    velog_stats["like_diff"] = diff_from_days_ago(history, 7, "total_likes")
    velog_stats["post_diff"] = diff_from_days_ago(history, 7, "total_posts")

    outputs = {
        "velog-summary.svg": builder.render_velog_summary(velog_stats),
        "velog-ranking.svg": builder.render_velog_ranking(velog_stats["top_posts"]),
        "velog-trend.svg": builder.render_velog_trend(history),
    }
    for name, svg in outputs.items():
        path = os.path.join(output_dir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        logger.info("Wrote %s", path)


def generate(args):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    demo = getattr(args, "demo", False)

    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yml")
    if demo:
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.example.yml")

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        logger.error("config.yml not found.")
        sys.exit(1)

    try:
        config = validate_config(config)
    except ConfigError as e:
        logger.error("Invalid config: %s", e)
        sys.exit(1)

    username = config["username"]
    logger.info("Generating profile SVGs for @%s...", username)

    if demo:
        logger.info("Demo mode: using hardcoded stats and languages.")
        stats = DEMO_STATS
        languages = DEMO_LANGUAGES
    else:
        api = GitHubAPI(username)

        logger.info("Fetching stats...")
        try:
            stats = api.fetch_stats()
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            logger.warning("Could not fetch stats (%s). Using defaults.", e)
            stats = {"commits": 0, "stars": 0, "prs": 0, "issues": 0, "repos": 0}

        logger.info("Fetching languages...")
        try:
            languages = api.fetch_languages()
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            logger.warning("Could not fetch languages (%s). Using defaults.", e)
            languages = {}

    logger.info("Stats: %s", stats)
    logger.info("Languages: %d found", len(languages))

    builder = SVGBuilder(config, stats, languages)
    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "generated")
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(output_dir, "tech-stack.svg")
    with open(path, "w") as f:
        f.write(builder.render_tech_stack())
    logger.info("Wrote %s", path)

    if not demo:
        generate_velog_cards(config, builder, output_dir)

    logger.info("Done!")


def main():
    parser = argparse.ArgumentParser(description="Generate Galaxy Profile SVGs")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Interactive setup wizard to create config.yml")

    gen_parser = subparsers.add_parser("generate", help="Generate SVGs from config")
    gen_parser.add_argument("--demo", action="store_true")

    parser.add_argument("--demo", action="store_true")

    args = parser.parse_args()

    if args.command == "init":
        from generator.cli_init import run_wizard
        run_wizard()
    else:
        generate(args)


if __name__ == "__main__":
    main()
