---
name: werss-mp-briefing
description: Generate objective morning/evening WeRSS briefing reports for the D91 `/mp`新增文章报告 module, with structured HTML-ready JSON for the website and Markdown for Obsidian archives. Use when Codex needs to create, debug, validate, or update WeRSS公众号早报/晚报, website新增文章报告, evidence-linked source summaries, or Obsidian archived briefing output.
---

# WeRSS MP Briefing

## Contract

Generate a site-facing briefing from WeRSS articles fetched in the fixed report slot window.

- Scope: D91 `/mp` 新增文章报告 only.
- Window: use WeRSS `articles.published_at`; keep fixed morning/evening slot cutoffs. Delayed generation changes `generated_at`, not `window_end`.
- Source basis: summarize from article body content. Use `description` only when body is empty and mark the limitation.
- Citations: use pure numeric source ids (`1`, `2`, ...). Display them as `「1」`; in the `来源` column each id must link to the original article URL, e.g. `[「1」](https://...)`.
- Content: stay factual and source-grounded. Do not invent facts, numbers, dates, tickers, sources, or conclusions.
- Themes: infer themes from the article batch; do not predefine the number or category list.
- Artifacts: produce synchronized Markdown for archive and structured JSON for website rendering.

## Output Shape

- `summary_table_json`: theme-level rows with `theme`, `core_viewpoint` or `summary_points`, and `sources`.
- `details_json`: theme-grouped `摘要速读` content and supporting source ids.
- `sources_json`: source id, article key, title, account, publish time, fetched time, original URL, section label, and evidence text when available.
- `report_markdown`: archive-ready Markdown with these sections:
  1. `# YYYY-MM-DD 早报/晚报`
  2. Metadata lines: report window, generated time, article count, account count
  3. `## 要点速览`: table with `主题 | 摘要 | 来源`
  4. `## 摘要速读`: grouped by the same inferred themes
  5. `## 引用来源`: numeric ids with original article links

## Writing Guidance

Goal: help readers understand what this batch of WeChat articles updated within about 3 minutes.

### 摘要

Use `摘要` as the fast-scanning layer inside the `要点速览` table.

- Keep it short and index-like: each theme should surface only the most important updates.
- Use concise points that merge similar views, remove repeated wording, and preserve distinct new information.
- Prefer direct declarative sentences grounded in the theme's source articles.

### 摘要速读

Use `摘要速读` as the readable briefing body, not a second copy of the table.

- Keep the same theme grouping, but explain what changed within each theme in fuller context.
- Add the relationships between updates, related companies/products/events when useful, and the theme's concrete scope.
- Write compact paragraphs or bullets that help the reader understand the batch without opening the source articles.
- Keep it objective and scannable; avoid direct copying from source text.

## Workflow

1. Identify the report slot: `morning` = 08:30, `evening` = 20:30, Asia/Shanghai.
2. Set `window_start` to the previous slot cutoff and `window_end` to the current slot cutoff. Morning covers previous-day 20:30 to current-day 08:30; evening covers current-day 08:30 to current-day 20:30.
3. Collect rows from WeRSS SQLite where `published_at > window_start AND published_at <= window_end`.
4. For each article, keep `id`, `title`, `account_name`, `url`, `publish_time`, `created_at`, `updated_at`, and enough body content to cite.
5. Build source ids (`1`, `2`, ...). Every theme, summary point, and detail section should reference source ids when using source-specific information.
6. Generate `summary_table_json`, `details_json`, `sources_json`, and `report_markdown` using the output shape above.
7. Validate source links, citation coverage, number grounding, and prohibited wording before writing or displaying the report.
8. Archive Markdown under `公众号早晚报/YYYY-MM/YYYY-MM-DD 早报.md` or `YYYY-MM-DD 晚报.md`.

## Output Requirements

Read `references/output_contract.md` before changing report fields, prompts, or validation.

Read `references/d91_integration.md` before changing `kuma.d91.global` backend/frontend behavior.

## Scripts

Collect a WeRSS window as JSON:

```bash
python3 scripts/collect_werss_window.py \
  --db "/Users/kumaai/Documents/New project 2/werss/data/werss-data/db.db" \
  --start "2026-06-16 08:30:00" \
  --end "2026-06-16 20:30:00" \
  --output /tmp/werss-window.json
```

Validate a structured report JSON:

```bash
python3 scripts/validate_report.py /tmp/report.json
```

## Quality Gates

- No source URL missing from `sources_json`.
- No theme row or detail section without source ids when articles are present.
- Every numeric token in generated summary/detail text should appear in one of the referenced source evidence texts.
- Markdown and JSON must describe the same title, window, source ids, and core sections.
- Empty windows should produce an explicit no-new-article report, not fabricated themes.
