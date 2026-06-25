---
name: werss-mp-briefing
description: Generate objective morning/evening WeRSS briefing reports for the D91 `/mp`新增文章报告 module, with structured HTML-ready JSON for the website and Markdown for Obsidian archives. Use when Codex needs to create, debug, or update WeRSS公众号早报/晚报, website新增文章报告, evidence-linked source summaries, or Obsidian archived briefing output.
---

# WeRSS MP Briefing

## Contract

Generate a site-facing briefing from WeRSS articles fetched in the fixed report slot window.

- Scope: D91 `/mp` 新增文章报告 only.
- Window: use the original article publish time (`articles.publish_time`) for fixed morning/evening slot inclusion. Delayed generation changes `generated_at`, not `window_end`.
- Source basis: summarize from article body content. Use `description` only when body is empty and mark the limitation.
- Content: stay factual and source-grounded. Do not invent facts, numbers, dates, tickers, sources, or conclusions.
- Themes: infer themes from the article batch; do not predefine the number or category list.
- Format: follow `references/output_contract.md`.

## Writing Guidance

Goal: help readers quickly understand what this batch of WeChat articles updated, without losing necessary context.

Write as direct synthesized information. Use the actual subject of the update as the sentence subject: company, product, technology, event, market, policy, or trend. Present what changed and how items relate to each other directly; citations identify sources separately and should not shape the prose.

### 摘要

Use `摘要` as the fast-scanning layer inside the `要点速览` table.

- Keep it scan-friendly: each theme should surface the most important updates without compressing away essential context.
- Use concise points that merge similar views, remove repeated wording, and preserve distinct new information.
- Prefer direct declarative sentences grounded in the referenced content.

### 摘要速读

Use `摘要速读` as the readable briefing body, not a second copy of the table.

- Keep the same theme grouping, but use the opening paragraph as theme-level synthesis.
- The opening paragraph should explain the broader change, shared context, or implication across the sources, rather than restating the bullets.
- Use bullets for concrete objects, events, numbers, source-backed details, and differences between sources.
- Retain companies, products, events, numbers, and conditions when needed for understanding.
- Keep it objective and scannable; avoid direct copying from source text.

## Workflow

1. Identify the report slot: `morning` = 08:30, `evening` = 20:30, Asia/Shanghai.
2. Set `window_start` to the previous slot cutoff and `window_end` to the current slot cutoff. Morning covers previous-day 20:30 to current-day 08:30; evening covers current-day 08:30 to current-day 20:30.
3. Collect rows from WeRSS SQLite where `publish_time > window_start AND publish_time <= window_end`.
4. For each article, keep `id`, `title`, `account_name`, `url`, `publish_time`, `created_at`, `updated_at`, and enough body content to cite.
5. Build source ids (`1`, `2`, ...). Every theme, summary point, and detail section should reference source ids when using source-specific information.
6. Generate `summary_table_json`, `details_json`, `sources_json`, and `report_markdown` using the output contract.
7. Archive Markdown under `公众号早晚报/YYYY-MM/YYYY-MM-DD 早报.md` or `YYYY-MM-DD 晚报.md`.

## Output Requirements

Follow `references/output_contract.md` for fields and formatting.

## Final Checks

- No source URL missing from `sources_json`.
- No theme row or detail section without source ids when articles are present.
- Markdown and JSON must describe the same title, window, source ids, and core sections.
- Empty windows should produce an explicit no-new-article report, not fabricated themes.
