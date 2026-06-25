#!/usr/bin/env python3
"""Collect WeRSS articles for an original publish-time window."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, help="Path to WeRSS db.db")
    parser.add_argument("--start", required=True, help="Window start, SQLite datetime text")
    parser.add_argument("--end", required=True, help="Window end, SQLite datetime text")
    parser.add_argument("--output", help="Output JSON path; stdout when omitted")
    parser.add_argument("--limit", type=int, default=500)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    db_path = Path(args.db).expanduser()
    if not db_path.exists():
        raise SystemExit(f"WeRSS DB not found: {db_path}")
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    with conn:
        rows = conn.execute(
            """
            SELECT a.id, a.mp_id, COALESCE(f.mp_name, a.mp_id, '') AS account_name,
                   a.title, a.url, a.description, a.publish_time, a.created_at, a.updated_at,
                   substr(a.content, 1, 120000) AS content_excerpt
            FROM articles a
            LEFT JOIN feeds f ON f.id = a.mp_id
            WHERE a.publish_time > ? AND a.publish_time <= ?
            ORDER BY a.publish_time ASC, a.created_at ASC
            LIMIT ?
            """,
            (args.start, args.end, args.limit),
        ).fetchall()
    payload = {
        "window_start": args.start,
        "window_end": args.end,
        "article_count": len(rows),
        "articles": [dict(row) for row in rows],
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).expanduser().write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
