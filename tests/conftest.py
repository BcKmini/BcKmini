"""Shared pytest fixtures."""

import pytest


SAMPLE_CONFIG = {
    "username": "testuser",
    "profile": {
        "name": "Test User",
        "tagline": "Software Engineer",
        "location": "Seoul, Korea",
        "bio": "Building things.",
        "philosophy": "make it simple.",
    },
    "social": {"email": "test@example.com"},
    "galaxy_arms": [
        {"name": "AI Engineering", "color": "synapse_cyan", "items": ["Python", "PyTorch", "LangChain"]},
        {"name": "Web & Backend", "color": "dendrite_violet", "items": ["FastAPI", "TypeScript", "Node.js"]},
        {"name": "DevOps", "color": "axon_amber", "items": ["Docker", "AWS", "GitHub Actions"]},
    ],
    "theme": {
        "void": "#0D1117",
        "nebula": "#130800",
        "star_dust": "#3d1500",
        "synapse_cyan": "#FF4500",
        "dendrite_violet": "#FF8C00",
        "axon_amber": "#8B0000",
        "text_bright": "#ffffff",
        "text_dim": "#d4a0a0",
        "text_faint": "#8b6060",
    },
    "stats": {"metrics": ["commits", "stars", "prs", "issues", "repos"]},
    "languages": {"exclude": ["HTML", "CSS", "Shell", "Makefile"], "max_display": 8},
}

SAMPLE_LANGUAGES = {
    "Python": 50000,
    "TypeScript": 30000,
    "JavaScript": 20000,
    "Go": 15000,
    "Rust": 10000,
    "HTML": 5000,
    "CSS": 3000,
    "Shell": 2000,
}

SAMPLE_STATS = {
    "commits": 342,
    "stars": 28,
    "prs": 15,
    "issues": 7,
    "repos": 22,
}

SAMPLE_VELOG_STATS = {
    "username": "testvelog",
    "total_views": 12345,
    "total_likes": 234,
    "total_posts": 18,
    "view_diff": 456,
    "like_diff": -3,
    "post_diff": 0,
    "top_posts": [
        {"title": "가장 인기있는 글", "url_slug": "popular-post", "released_at": "2026-01-01", "views": 5000, "likes": 100},
        {"title": "두번째로 인기있는 글", "url_slug": "second-post", "released_at": "2026-01-05", "views": 3000, "likes": 60},
    ],
    "recent_posts": [
        {"title": "가장 최근에 쓴 글", "url_slug": "latest-post", "released_at": "2026-01-15", "views": 800, "likes": 20},
        {"title": "그 전에 쓴 글", "url_slug": "prior-post", "released_at": "2026-01-05", "views": 3000, "likes": 60},
    ],
}

SAMPLE_VELOG_HISTORY = [
    {"date": "2026-01-01", "total_views": 10000, "total_likes": 200, "total_posts": 17},
    {"date": "2026-01-08", "total_views": 11200, "total_likes": 215, "total_posts": 17},
    {"date": "2026-01-15", "total_views": 12345, "total_likes": 234, "total_posts": 18},
]


@pytest.fixture
def sample_config():
    return SAMPLE_CONFIG


@pytest.fixture
def sample_languages():
    return SAMPLE_LANGUAGES


@pytest.fixture
def sample_stats():
    return SAMPLE_STATS


@pytest.fixture
def sample_velog_stats():
    return SAMPLE_VELOG_STATS


@pytest.fixture
def sample_velog_history():
    return SAMPLE_VELOG_HISTORY
