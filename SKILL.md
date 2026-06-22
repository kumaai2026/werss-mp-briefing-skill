---
name: werss-mp-briefing
description: Generate objective morning/evening WeRSS briefing reports for the D91 `/mp`新增文章报告 module, with structured HTML-ready JSON for the website and Markdown for Obsidian archives. Use when Codex needs to create, debug, validate, or update WeRSS公众号早报/晚报, website新增文章报告, evidence-linked source summaries, or Obsidian archived briefing output.
---

# WeRSS MP Briefing

## Contract

Generate a site-facing briefing from WeRSS articles fetched in the fixed report slot window.

- Scope only D91 `/mp` 新增文章报告; do not use or extend the Feishu/Bitable daily report workflow.
- Use WeRSS `articles.publish_time` as the inclusion window. It is the original article time stored as Unix seconds. `created_at` and `updated_at` are crawler/database record times and must not decide report membership.
- Keep report windows fixed to slot cutoffs. Delayed generation changes `generated_at`, not `window_end`.
- Public report metadata must use readable Chinese labels: `报告窗口：2026年6月20日 08:30-20:30（北京时间）` or cross-day `至` format, and `收录文章：X 篇；来源公众号：Y 个`. Do not render `生成时间` in the public report.
- Derive summaries and evidence from article body content. Ignore WeRSS `description` unless the body is empty and label the limitation.
- Include original source links for every article used.
- Treat WeRSS article body as the default source of truth. When the body is missing, too short, or only a secondary digest, label that limitation instead of writing as if the original was verified.
- When an article contains primary links such as papers, filings, official releases, transcripts, or code repositories, use those primary links to verify important numbers, dates, names, and technical claims.
- Keep the copy objective and factual. Do not invent facts, numbers, dates, tickers, sources, or conclusions.
- Core viewpoints and detail summaries should synthesize the common point of each theme. Do not simply paste the first article digest or concatenate source sentences.
- Classify themes by the article's primary subject and domain anchors in the title/body. Incidental words such as `价格`, `市场`, `融资`, `估值`, `营收`, `亏损`, `安全`, or `风险` must not move an AI model, semiconductor hardware, software engineering, infrastructure, or market-record article into the wrong high-level theme unless the article's main subject is financial results, valuation, funding, macro policy, asset pricing, policy, security, or compliance.
- Output the synthesis directly. Do not start with introductory wrappers such as `XX主题下`, `文章集中讨论`, `共同线索是`, `共同指向`, or `本时段核心不是单篇消息本身`.
- Avoid vague, low-information summaries. Each core viewpoint must state the concrete logic, constraint, change, or evidence boundary shown by the referenced articles.
- Treat the report as finite-sample information organization, not as industry trend research. Do not generalize a single article or a small same-account group into `趋势`, `格局变化`, `核心变化`, or `商业化叙事`.
- Use conclusion-strength labels when writing summaries:
  - `single_source_fact`: one source only; write `单篇文章显示`, `原文称`, or `该报告披露`, and do not infer a sector-level conclusion.
  - `multi_source_same_topic`: two to three sources, or sources from one account only; write that multiple articles involve the same topic, but do not claim a trend.
  - `cross_source_pattern`: at least three sources from at least two accounts; only then use limited phrasing such as `本时段样本显示`.
- Prefer concrete facts, differences, and source boundaries over abstract explanations. If evidence bullets already contain the useful facts, do not add a generic introductory summary.
- `摘要速读` is not a one-sentence topic label. Each public evidence bullet should extract the article's valuable contents: named counterparties, product routes, technical parameters, quantified targets, constraints, or stated cause-effect links when present in the body. Avoid bullets that only say the article `讨论/介绍/复盘` a topic without the actual facts.
- Use an article-card intermediate layer when model-assisted summarization is enabled. Each card should contain `main_point`, `key_facts`, `entities`, `topic_hint`, and `quality_flags`. If model output is unavailable or invalid, fall back to deterministic extraction and keep the same public contract.
- In the public Markdown/HTML report, name the detail section `摘要速读`, not `事实摘录与有限归纳`. Do not render generic theme-opening paragraphs or disclaimer-like sentences such as `下方逐篇列出代表文章主旨`, `不替代交易结论`, or `不外推到板块或行业层面`.
- Name the summary table column `摘要`, not `要点摘要`.
- Public citations must use numeric paper-style labels such as `[1]`, `[2]`, and `[3]`; do not expose internal ids such as `S1` or `[S1]` in public Markdown/HTML. Add a short note: `引用说明：文中方括号数字对应文末“参考文献”。`
- Name the public source section `参考文献`. Render each public source as `[1] 公众号名. 文章标题[EB/OL]. 微信公众号. 原文链接`; do not append publish timestamps in that public reference list.
- Do not render public disclaimers such as `说明：本报告为客观信息整理，不提供行动建议`.
- If a public evidence point intentionally uses a direct source sentence, render it as a Markdown blockquote or HTML `<blockquote>`; otherwise use formal paraphrase.
- Use formal research-record style. Clean public evidence bullets to remove colloquial, emotional, headline-like, or rhetorical wording while preserving entities, numbers, dates, and source ids.
- Do not provide investment advice or action language such as `投资建议`, `推荐`, `买入`, `关注方向`, or `配置建议`.
- Produce two synchronized artifacts:
  - Markdown for Obsidian archival.
  - Structured JSON fields for website rendering.

## Workflow

1. Identify the report slot: `morning` = 08:30, `evening` = 20:30, Asia/Shanghai.
2. Set `window_start` to the previous slot cutoff and `window_end` to the current slot cutoff. Morning covers previous-day 20:30 to current-day 08:30; evening covers current-day 08:30 to current-day 20:30.
3. Collect rows from WeRSS SQLite where `publish_time > window_start_unix_seconds AND publish_time <= window_end_unix_seconds`, interpreting `window_start` and `window_end` in Asia/Shanghai.
4. For each article, keep `id`, `title`, `account_name`, `url`, `publish_time`, `created_at`, `updated_at`, and enough body content to cite.
5. Build internal source ids (`S1`, `S2`, ...) for validation and compatibility, and also attach public `citation_index` / `citation_label` values such as `1` / `[1]`. Every table row and detail section must reference one or more internal source ids, but public rendering must map them to numeric labels.
6. Assign themes using primary-subject classification:
   - Treat strong domain anchors such as model names/platforms, semiconductor components/materials, compute infrastructure, software engineering terms, policy actors, and robotics terms as the main signal.
   - Treat broad business or risk words such as `市场`, `价格`, `融资`, `估值`, `安全`, and `风险` as secondary unless the title and evidence are mainly about financial statements, funding rounds, valuation, macro rates, asset repricing, policy, security, or compliance.
   - Audit the largest groups for mixed subjects. If one group contains unrelated AI-model, hardware-material, and macro/company-finance articles only because they share business words, reassign by domain.
7. Run a source verification pass:
   - Mark whether the WeRSS body is available and long enough to support the article.
   - Open or preserve the original URL where possible.
   - Verify primary links embedded in the article for high-impact numbers, dates, named entities, and technical claims.
   - Mark unavailable originals, secondary-only evidence, duplicate sources, and conflicts in internal quality warnings or `source_audit_json`.
8. Compare final draft claims against source evidence before publishing. Each `core_viewpoint`, `details.summary`, and evidence bullet must be supported by the referenced source body or clearly labeled as a synthesis within the evidence boundary.
9. Generate:
   - `summary_table_json`: rows with `theme`, `core_viewpoint`, and `sources`.
   - `details_json`: sections with `theme`, optional `summary`, `evidence_points`, `sources`, `source_count`, `account_count`, and `conclusion_strength`. Leave `summary` empty when it would only repeat a generic theme disclaimer.
   - `sources_json`: source id, title, account, publish time, fetched time, original URL.
   - optional `source_audit_json`: claim-level source comparison for debugging and archive QA.
   - `report_markdown`: archive-ready Markdown matching the JSON.
10. Validate source links, citation coverage, number grounding, source comparison, theme fit, and prohibited wording before writing or displaying the report.
11. Archive Markdown under `公众号早晚报/YYYY-MM/YYYY-MM-DD 早报.md` or `YYYY-MM-DD 晚报.md`.

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
- No article should be grouped under `金融市场与公司经营` solely because the source text mentions prices, market size, funding, valuation, revenue, or losses when the article's primary subject is an AI model/product, semiconductor hardware/material, compute infrastructure, software engineering, policy event, or robotics topic.
- No `summary_table_json` row without at least one source id.
- No `details_json` evidence point without a source id.
- Every numeric token in generated table/detail text must appear in one of the referenced source evidence texts.
- Important named entities, dates, transaction amounts, model names, securities codes, and research results must be traceable to source body text or primary links.
- Final summary wording must not upgrade unverified source labels into verified original facts.
- Public report text must not contain over-generalization phrases such as `核心变化`, `趋势`, `行业格局`, `商业化叙事`, `产业链支撑`, or `价值重估`.
- Public report text must not contain empty templates such as `判断依据在于`, `是否支撑`, `这些信息支持的结论限于`, or `关键证据在于`.
- Public report text must not contain colloquial or emotional wording such as `狂烧`, `这才`, `啥`, `一项项`, `触目惊心`, `一次性垃圾`, repeated ellipses, or rhetorical questions.
- Public report Markdown/HTML must not render `生成时间`, `新增文章：`, or the disclaimer `说明：本报告为客观信息整理，不提供行动建议`.
- Public report Markdown/HTML must use `收录文章：X 篇；来源公众号：Y 个`, table header `主题 | 摘要 | 来源`, and the numeric-reference explanation `引用说明：文中方括号数字对应文末“参考文献”。`
- Public report Markdown/HTML must not expose `S1`, `S2`, `[S1]`, or `[S2]`; internal source ids may remain in JSON for validation, but public rendering must use `[1]`, `[2]`, etc.
- Public report text must not expose low-signal metadata snippets such as `公开发表于`, `原始内容参考`, `内容提要`, `报告文章摘要概述`, `投资逻辑`, `导语`, `今日好文`, `原文正面表述`, or first-person process fragments such as `比如，我`, `我一查`, `我本来顺手`, `试探性激将`, `过程就不展示`, `并且当然`.
- Public evidence bullets must not collapse rich article bodies into direction-only statements such as `在访谈中讨论英特尔代工、产品路线和长期回报目标`; include the actual cooperation parties, route parameters, and targets when the body provides them.
- Markdown and JSON must describe the same title, window, source ids, and core sections.
- Keep evidence-boundary disclosures in `quality_warnings_json` and optional `source_audit_json`; do not render a public `信息边界` section in the final Markdown report unless the user explicitly asks for a debug/audit view.
- `quality_warnings_json` must include counts for single-source themes, themes without cross-source conclusions, and themes downgraded to fact excerpts.
- Empty windows should produce an explicit no-new-article report, not fabricated themes.
