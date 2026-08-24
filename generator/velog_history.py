"""Local JSON snapshot history for Velog stats.

There's no database here, so daily snapshots are appended to a small JSON
file committed alongside the generated SVGs. That's enough history to draw
a trend chart and compute N-day deltas without any external storage.
"""

import json
import os
from datetime import date

MAX_HISTORY_DAYS = 90


def load_history(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def update_history(path: str, stats: dict, today: str = None) -> list[dict]:
    """오늘자 스냅샷을 추가(또는 갱신)하고 파일에 반영한 뒤 전체 히스토리를 반환한다."""
    today = today or date.today().isoformat()

    history = load_history(path)
    history = [h for h in history if h["date"] != today]
    history.append(
        {
            "date": today,
            "total_views": stats["total_views"],
            "total_likes": stats["total_likes"],
            "total_posts": stats["total_posts"],
        }
    )
    history.sort(key=lambda h: h["date"])
    history = history[-MAX_HISTORY_DAYS:]

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    return history


def diff_from_days_ago(history: list[dict], days: int, key: str) -> int:
    """가장 최근 값과 days일 전(또는 가장 오래된) 값의 차이를 반환한다."""
    if len(history) < 2:
        return 0
    latest = history[-1][key]
    idx = max(len(history) - 1 - days, 0)
    baseline = history[idx][key]
    return latest - baseline
