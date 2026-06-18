#!/usr/bin/env python3
"""Validate a D91 WeRSS briefing report JSON payload."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PROHIBITED = ("投资建议", "推荐买入", "买入评级", "卖出评级", "关注方向", "配置建议", "目标价")
LOW_INFORMATION_WRAPPERS = (
    "XX主题下",
    "文章集中讨论",
    "共同线索是",
    "共同指向",
    "本时段核心不是单篇消息本身",
    "从来源分布看",
    "可比的信息不是标题热度",
)
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:%|pct|bp|bps|万|亿|元|美元|人民币|GB|TB|PB|MW|GW|kW|W|卡时|颗|篇|个|家|倍)?")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_json")
    return parser.parse_args()


def text_numbers(value: str) -> set[str]:
    return {re.sub(r"\s+", "", item.group(0)) for item in NUMBER_RE.finditer(value or "")}


def main() -> int:
    args = parse_args()
    payload = json.loads(Path(args.report_json).read_text(encoding="utf-8"))
    findings: list[str] = []
    sources = payload.get("sources_json") or payload.get("sources") or []
    source_map = {str(item.get("id")): item for item in sources if isinstance(item, dict)}
    if not source_map and (payload.get("article_count") or 0) > 0:
        findings.append("sources_json is empty")
    for source in sources:
        if not source.get("url"):
            findings.append(f"{source.get('id', '?')} missing url")
    generated_text = json.dumps(
        {
            "summary_table_json": payload.get("summary_table_json"),
            "details_json": payload.get("details_json"),
        },
        ensure_ascii=False,
    )
    for phrase in PROHIBITED:
        if phrase in generated_text:
            findings.append(f"prohibited phrase: {phrase}")
    for phrase in LOW_INFORMATION_WRAPPERS:
        if phrase in generated_text:
            findings.append(f"low-information wrapper: {phrase}")
    for row in payload.get("summary_table_json") or []:
        refs = [str(item) for item in row.get("sources") or []]
        if not refs:
            findings.append(f"summary row missing sources: {row.get('theme', '')}")
        evidence = " ".join(str(source_map.get(ref, {}).get("evidence_text") or "") for ref in refs)
        missing = text_numbers(str(row.get("core_viewpoint") or "")) - text_numbers(evidence)
        if missing:
            findings.append(f"summary row ungrounded numbers {sorted(missing)}: {row.get('theme', '')}")
    for detail in payload.get("details_json") or []:
        refs = [str(item) for item in detail.get("sources") or []]
        if not refs:
            findings.append(f"detail missing sources: {detail.get('theme', '')}")
        for point in detail.get("evidence_points") or []:
            point_refs = [str(item) for item in point.get("sources") or refs]
            evidence = " ".join(str(source_map.get(ref, {}).get("evidence_text") or "") for ref in point_refs)
            missing = text_numbers(str(point.get("text") or "")) - text_numbers(evidence)
            if missing:
                findings.append(f"evidence point ungrounded numbers {sorted(missing)}: {detail.get('theme', '')}")
    result = {"ok": not findings, "findings": findings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
