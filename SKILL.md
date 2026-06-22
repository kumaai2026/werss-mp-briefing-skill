---
name: werss-mp-briefing
description: Generate objective morning/evening WeRSS briefing reports for the D91 `/mp`新增文章报告 module, with structured HTML-ready JSON for the website and Markdown for Obsidian archives. Use when Codex needs to create, debug, validate, or update WeRSS公众号早报/晚报, website新增文章报告, evidence-linked source summaries, or Obsidian archived briefing output.
---

# WeRSS MP Briefing

## Contract

Generate a site-facing briefing from WeRSS articles fetched in the fixed report slot window.

- Scope only D91 `/mp` 新增文章报告; do not use or extend the Feishu/Bitable daily report workflow.
- Use WeRSS `articles.created_at` as the inclusion window. `publish_time` is display metadata only.
- Keep report windows fixed to slot cutoffs. Delayed generation changes `generated_at`, not `window_end`.
- Derive summaries and evidence from article body content. Ignore WeRSS `description` unless the body is empty and label the limitation.
- Include original source links for every article used.
- Treat WeRSS article body as the default source of truth. When the body is missing, too short, or only a secondary digest, label that limitation instead of writing as if the original was verified.
- When an article contains primary links such as papers, filings, official releases, transcripts, or code repositories, use those primary links to verify important numbers, dates, names, and technical claims.
- Keep the copy objective and factual. Do not invent facts, numbers, dates, tickers, sources, or conclusions.
- Core viewpoints and detail summaries should synthesize the common point of each theme. Do not simply paste the first article digest or concatenate source sentences.
- Output the synthesis directly. Do not start with introductory wrappers such as `XX主题下`, `文章集中讨论`, `共同线索是`, `共同指向`, or `本时段核心不是单篇消息本身`.
- Avoid vague, low-information summaries. Each core viewpoint must state the concrete logic, constraint, change, or evidence boundary shown by the referenced articles.
- Do not provide investment advice or action language such as `投资建议`, `推荐`, `买入`, `关注方向`, or `配置建议`.
- Produce two synchronized artifacts:
  - Markdown for Obsidian archival.
  - Structured JSON fields for website rendering.

## Workflow

1. Identify the report slot: `morning` = 08:30, `evening` = 20:30, Asia/Shanghai.
2. Set `window_start` to the previous slot cutoff and `window_end` to the current slot cutoff. Morning covers previous-day 20:30 to current-day 08:30; evening covers current-day 08:30 to current-day 20:30.
3. Collect rows from WeRSS SQLite where `created_at > window_start AND created_at <= window_end`.
4. For each article, keep `id`, `title`, `account_name`, `url`, `publish_time`, `created_at`, `updated_at`, and enough body content to cite.
5. Build source ids (`S1`, `S2`, ...). Every table row and detail section must reference one or more source ids.
6. Run a source verification pass:
   - Mark whether the WeRSS body is available and long enough to support the article.
   - Open or preserve the original URL where possible.
   - Verify primary links embedded in the article for high-impact numbers, dates, named entities, and technical claims.
   - Mark unavailable originals, secondary-only evidence, duplicate sources, and conflicts for `信息边界`.
7. Compare final draft claims against source evidence before publishing. Each `core_viewpoint`, `details.summary`, and evidence bullet must be supported by the referenced source body or clearly labeled as a synthesis within the evidence boundary.
8. Generate:
   - `summary_table_json`: rows with `theme`, `core_viewpoint`, and `sources`.
   - `details_json`: sections with `theme`, `summary`, `evidence_points`, and `sources`.
   - `sources_json`: source id, title, account, publish time, fetched time, original URL.
   - optional `source_audit_json`: claim-level source comparison for debugging and archive QA.
   - `report_markdown`: archive-ready Markdown matching the JSON.
9. Validate source links, citation coverage, number grounding, source comparison, and prohibited wording before writing or displaying the report.
10. Archive Markdown under `公众号早晚报/YYYY-MM/YYYY-MM-DD 早报.md` or `YYYY-MM-DD 晚报.md`.

## Output Requirements

Read `references/output_contract.md` before changing report fields, prompts, or validation.

Read `references/source_verification_audit.md` before changing source-grounding, claim-audit, or final-summary comparison behavior.

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
- No `summary_table_json` row without at least one source id.
- No `details_json` evidence point without a source id.
- Every numeric token in generated table/detail text must appear in one of the referenced source evidence texts.
- Important named entities, dates, transaction amounts, model names, securities codes, and research results must be traceable to source body text or primary links.
- Final summary wording must not upgrade unverified source labels into verified original facts.
- Markdown and JSON must describe the same title, window, source ids, and core sections.
- `信息边界` must disclose missing article bodies, secondary-only sources, duplicate/derivative sources, and important excluded claims.
- Empty windows should produce an explicit no-new-article report, not fabricated themes.
