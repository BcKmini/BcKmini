"""Velog GraphQL client — independent implementation, no dependency on any
third-party velog-statistics service. Auth is done the same way velog.io's
own web client does it: an access_token/refresh_token pair sent as cookies.
"""

import logging
import os

import requests

logger = logging.getLogger(__name__)

V3_URL = "https://v3.velog.io/graphql"
V2_CDN_URL = "https://v2cdn.velog.io/graphql"

POSTS_QUERY = """
    query velogPosts($input: GetPostsInput!) {
        posts(input: $input) {
            id
            title
            url_slug
            likes
            released_at
        }
    }
"""

POST_STATS_QUERY = """
    query GetStats($post_id: ID!) {
        getStats(post_id: $post_id) {
            total
        }
    }
"""


class VelogError(RuntimeError):
    """Raised when a Velog API request fails or returns an unexpected shape."""


class VelogClient:
    def __init__(self, username: str, access_token: str = None, refresh_token: str = None):
        self.username = username
        self.access_token = access_token or os.environ.get("VELOG_ACCESS_TOKEN", "")
        self.refresh_token = refresh_token or os.environ.get("VELOG_REFRESH_TOKEN", "")
        if not self.access_token or not self.refresh_token:
            raise VelogError("VELOG_ACCESS_TOKEN / VELOG_REFRESH_TOKEN이 설정되지 않았습니다.")

    def _headers(self) -> dict:
        return {
            "authority": "v3.velog.io",
            "origin": "https://velog.io",
            "content-type": "application/json",
            "cookie": f"access_token={self.access_token}; refresh_token={self.refresh_token}",
        }

    def _post(self, url: str, query: str, variables: dict = None, operation_name: str = None) -> dict:
        payload = {"query": query}
        if variables is not None:
            payload["variables"] = variables
        if operation_name:
            payload["operationName"] = operation_name

        resp = requests.post(url, json=payload, headers=self._headers(), timeout=15)
        if resp.status_code != 200:
            raise VelogError(f"Velog API HTTP {resp.status_code}: {resp.text[:200]}")

        body = resp.json()
        if "errors" in body:
            raise VelogError(f"Velog GraphQL error: {body['errors']}")

        data = body.get("data")
        if not isinstance(data, dict):
            raise VelogError("Velog API가 예상치 못한 응답을 반환했습니다.")
        return data

    def fetch_all_posts(self) -> list[dict]:
        """페이지네이션을 자동으로 처리해 모든 게시글을 가져온다."""
        cursor = ""
        posts: list[dict] = []
        for _ in range(100):  # 안전장치: 최대 5000개 (50 * 100)
            variables = {"input": {"cursor": cursor, "username": self.username, "limit": 50, "tag": ""}}
            data = self._post(V3_URL, POSTS_QUERY, variables)
            batch = data.get("posts") or []
            if not batch:
                break
            posts.extend(batch)
            cursor = batch[-1].get("id", "")
            if not cursor:
                break
        return posts

    def fetch_post_views(self, post_id: str) -> int:
        try:
            data = self._post(V2_CDN_URL, POST_STATS_QUERY, {"post_id": post_id}, "GetStats")
            stats = data.get("getStats") or {}
            return int(stats.get("total", 0) or 0)
        except VelogError as e:
            logger.warning("게시글 조회수 조회 실패 (post_id=%s): %s", post_id, e)
            return 0

    def fetch_user_stats(self) -> dict:
        """전체 게시글 + 게시글별 조회수/좋아요를 모아 요약 통계를 만든다."""
        posts = self.fetch_all_posts()

        enriched = []
        total_views = 0
        total_likes = 0
        for post in posts:
            views = self.fetch_post_views(post["id"])
            likes = int(post.get("likes", 0) or 0)
            total_views += views
            total_likes += likes
            enriched.append(
                {
                    "title": post.get("title") or "(제목 없음)",
                    "url_slug": post.get("url_slug", ""),
                    "released_at": post.get("released_at", ""),
                    "views": views,
                    "likes": likes,
                }
            )

        top_posts = sorted(enriched, key=lambda p: p["views"], reverse=True)[:5]
        recent_posts = sorted(enriched, key=lambda p: p["released_at"] or "", reverse=True)[:5]

        return {
            "username": self.username,
            "total_views": total_views,
            "total_likes": total_likes,
            "total_posts": len(posts),
            "top_posts": top_posts,
            "recent_posts": recent_posts,
        }
