#!/usr/bin/env python3
"""Validate a D91 WeRSS briefing report JSON payload."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PROHIBITED = (
    "投资建议",
    "投资影响",
    "投资机会",
    "推荐买入",
    "推荐：",
    "买入评级",
    "卖出评级",
    "关注方向",
    "配置建议",
    "受益：",
    "受益标的",
    "价值重估",
    "目标价",
)
LOW_INFORMATION_WRAPPERS = (
    "XX主题下",
    "文章集中讨论",
    "共同线索是",
    "共同指向",
    "本时段核心不是单篇消息本身",
    "从来源分布看",
    "可比的信息不是标题热度",
)
OVERGENERALIZATION_PHRASES = (
    "核心变化",
    "趋势",
    "行业格局",
    "格局变化",
    "商业化叙事",
    "产业链支撑",
    "价值重估",
)
EMPTY_SUMMARY_TEMPLATES = (
    "判断依据在于",
    "是否支撑",
    "这些信息支持的结论限于",
    "关键证据在于",
    "数字、日期和具体事实以证据句",
)
COLLOQUIAL_PHRASES = (
    "狂烧",
    "这才",
    "啥",
    "一项项",
    "……",
    "…",
    "比如，我",
    "试探性激将",
    "过程就不展示",
    "并且当然",
    "我一查",
    "我本来顺手",
    "为几个数字较真",
)
LOW_SIGNAL_SUMMARY_PHRASES = (
    "公开发表于",
    "原始内容参考",
    "内容提要",
    "youtube.com",
    "youtu.be",
)
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:%|pct|bp|bps|万|亿|元|美元|人民币|GB|TB|PB|MW|GW|kW|W|卡时|颗|篇|个|家|倍)?")
SOURCE_LINE_RE = re.compile(r"^- \[S\d+\] .+（公众号：.+）$")
AUDIT_STATUSES = {"supported", "partial", "unverified", "conflict"}
CONCLUSION_STRENGTHS = {"single_source_fact", "multi_source_same_topic", "cross_source_pattern"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_json")
    return parser.parse_args()


def text_numbers(value: str) -> set[str]:
    return {re.sub(r"\s+", "", item.group(0)) for item in NUMBER_RE.finditer(value or "")}


def append_unknown_refs(findings: list[str], refs: list[str], source_map: dict[str, dict], label: str) -> None:
    unknown = [ref for ref in refs if ref not in source_map]
    if unknown:
        findings.append(f"{label} unknown sources: {sorted(unknown)}")


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
    for phrase in OVERGENERALIZATION_PHRASES:
        if phrase in generated_text:
            findings.append(f"over-generalization phrase: {phrase}")
    for phrase in EMPTY_SUMMARY_TEMPLATES:
        if phrase in generated_text:
            findings.append(f"empty summary template: {phrase}")
    for phrase in COLLOQUIAL_PHRASES:
        if phrase in generated_text:
            findings.append(f"colloquial phrase: {phrase}")
    for phrase in LOW_SIGNAL_SUMMARY_PHRASES:
        if phrase in generated_text:
            findings.append(f"low-signal summary phrase: {phrase}")
    if re.search(r"[?？]", generated_text):
        findings.append("rhetorical question punctuation")
    markdown = str(payload.get("report_markdown") or "")
    if markdown:
        if "生成时间：" in markdown:
            findings.append("markdown exposes generated time")
        if "新增文章：" in markdown:
            findings.append("markdown uses ambiguous 新增文章 metadata")
        if "说明：本报告为客观信息整理" in markdown:
            findings.append("markdown contains public disclaimer")
        if "| 主题 | 要点摘要 | 来源 |" in markdown:
            findings.append("markdown uses old summary table heading")
        if (payload.get("article_count") or 0) > 0 and "| 主题 | 摘要 | 来源 |" not in markdown:
            findings.append("markdown missing summary table heading")
        if (payload.get("article_count") or 0) > 0 and ("收录文章：" not in markdown or "来源公众号：" not in markdown):
            findings.append("markdown missing collection/source account metadata")
        if (payload.get("article_count") or 0) > 0 and "引用编号：" not in markdown:
            findings.append("markdown missing source id explanation")
        if "## 事实摘录与有限归纳" in markdown:
            findings.append("markdown uses old detail heading")
        if "## 来源清单" in markdown:
            findings.append("markdown uses old source heading")
        if (payload.get("article_count") or 0) > 0 and "## 摘要速读" not in markdown:
            findings.append("markdown missing 摘要速读 heading")
        if (payload.get("article_count") or 0) > 0 and "## 引用来源" not in markdown:
            findings.append("markdown missing 引用来源 heading")
        for phrase in ("下方逐篇列出代表文章主旨", "不替代交易结论", "不外推到板块或行业层面"):
            if phrase in markdown:
                findings.append(f"markdown contains generic body disclaimer: {phrase}")
        source_section = markdown.split("## 引用来源", 1)[1] if "## 引用来源" in markdown else ""
        source_lines = [line for line in source_section.splitlines() if line.startswith("- [S")]
        for source in sources:
            source_id = str(source.get("id") or "")
            if source_id and not any(line.startswith(f"- [{source_id}] ") for line in source_lines):
                findings.append(f"markdown missing citation line: {source_id}")
        for line in source_lines:
            if not SOURCE_LINE_RE.match(line):
                findings.append(f"markdown citation format invalid: {line[:80]}")
            if re.search(r"(?:19|20)\d{2}-\d{2}-\d{2}T\d{2}:\d{2}", line):
                findings.append(f"markdown citation contains timestamp: {line[:80]}")
    for row in payload.get("summary_table_json") or []:
        refs = [str(item) for item in row.get("sources") or []]
        if not refs:
            findings.append(f"summary row missing sources: {row.get('theme', '')}")
        append_unknown_refs(findings, refs, source_map, f"summary row {row.get('theme', '')}")
        evidence = " ".join(str(source_map.get(ref, {}).get("evidence_text") or "") for ref in refs)
        missing = text_numbers(str(row.get("core_viewpoint") or "")) - text_numbers(evidence)
        if missing:
            findings.append(f"summary row ungrounded numbers {sorted(missing)}: {row.get('theme', '')}")
    for detail in payload.get("details_json") or []:
        refs = [str(item) for item in detail.get("sources") or []]
        if not refs:
            findings.append(f"detail missing sources: {detail.get('theme', '')}")
        append_unknown_refs(findings, refs, source_map, f"detail {detail.get('theme', '')}")
        strength = str(detail.get("conclusion_strength") or "")
        if strength and strength not in CONCLUSION_STRENGTHS:
            findings.append(f"detail invalid conclusion_strength: {strength}")
        if strength == "single_source_fact" and len(set(refs)) != 1:
            findings.append(f"single_source_fact source count mismatch: {detail.get('theme', '')}")
        if strength == "cross_source_pattern" and len(set(refs)) < 3:
            findings.append(f"cross_source_pattern source count too small: {detail.get('theme', '')}")
        evidence = " ".join(str(source_map.get(ref, {}).get("evidence_text") or "") for ref in refs)
        missing = text_numbers(str(detail.get("summary") or "")) - text_numbers(evidence)
        if missing:
            findings.append(f"detail summary ungrounded numbers {sorted(missing)}: {detail.get('theme', '')}")
        for point in detail.get("evidence_points") or []:
            point_refs = [str(item) for item in point.get("sources") or refs]
            append_unknown_refs(findings, point_refs, source_map, f"evidence point {detail.get('theme', '')}")
            evidence = " ".join(str(source_map.get(ref, {}).get("evidence_text") or "") for ref in point_refs)
            missing = text_numbers(str(point.get("text") or "")) - text_numbers(evidence)
            if missing:
                findings.append(f"evidence point ungrounded numbers {sorted(missing)}: {detail.get('theme', '')}")
    for item in payload.get("source_audit_json") or []:
        status = str(item.get("status") or "")
        if status not in AUDIT_STATUSES:
            findings.append(f"source audit invalid status: {status or '?'}")
        refs = [str(ref) for ref in item.get("sources") or []]
        if not refs:
            findings.append(f"source audit missing sources: {str(item.get('claim') or '')[:40]}")
        append_unknown_refs(findings, refs, source_map, "source audit")
    result = {"ok": not findings, "findings": findings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
