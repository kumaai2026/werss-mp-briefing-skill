# Output Contract

Use these JSON fields for D91 website rendering.

## summary_table_json

Array of objects:

- `theme`: short factual topic name based on the article's primary subject. Prefer domain anchors from title/body. Do not classify an AI model/product, semiconductor hardware/material, compute infrastructure, software engineering, market-record, policy, or robotics article into a broad high-level theme only because it mentions prices, market size, funding, valuation, revenue, losses, safety, or risk.
- `core_viewpoint`: evidence-grounded key-point summary. It must state a concrete fact, difference, or source boundary, not a broad trend. For single-source rows, use `单篇文章显示`, `原文称`, or `该报告披露`; for weak multi-source rows, use `多篇文章共同涉及`; use `本时段样本显示` only when the row has at least three sources from at least two accounts. Keep numbers only when present in referenced sources.
- `sources`: array of internal source ids such as `["S1", "S3"]`. Public rendering must map these ids to numeric citation labels such as `[1]` and `[3]`.

## details_json

Array of objects:

- `theme`: same topic name used in the table when possible, with the same primary-subject classification rule.
- `summary`: objective finite-sample summary from referenced article bodies. It must contain a concrete object, action, number, or boundary. If evidence points already contain the useful facts, keep this to one short boundary sentence rather than adding a generic setup paragraph.
- `evidence_points`: array of `{ "text": "...", "sources": ["S1"] }`. Each public point should extract article value, not merely label the topic. When the body provides counterparties, product route, technical parameters, quantified targets, constraints, or stated cause-effect links, include those concrete details. Optional `quote` or `is_quote` may be true only when `text` intentionally preserves a direct original sentence for blockquote rendering. Public citation labels must be numeric, not `S`-prefixed.
- `sources`: unique source ids used by this detail section.
- `source_count`: count of unique source ids.
- `account_count`: count of unique source accounts.
- `conclusion_strength`: `single_source_fact`, `multi_source_same_topic`, or `cross_source_pattern`.

## sources_json

Array of objects:

- `id`: `S1`, `S2`, ...
- `citation_index`: integer public reference number, starting from 1.
- `citation_label`: numeric public label such as `[1]`.
- `article_key`
- `title`
- `account_name`
- `publish_time`
- `fetched_at`
- `url`
- `section_label`
- `evidence_text`: trimmed text used only for validation/debugging. The website may omit or hide it.

## source_audit_json

Optional debug/archive array. Use when claims require final-summary-to-source comparison.

- `claim`: generated claim being checked.
- `claim_location`: `summary_table_json`, `details_json.summary`, or `details_json.evidence_points`.
- `sources`: source ids used to support the claim.
- `status`: one of `supported`, `partial`, `unverified`, or `conflict`.
- `supporting_text`: short source excerpt, primary-source note, or explanation of why the original is missing.
- `notes`: concise boundary note, such as `secondary-only source`, `primary link verified`, `duplicate source`, or `number excluded`.

Do not render this field as a public website section by default. Use it together with `quality_warnings_json` for internal QA and optional audit views.

## report_markdown

Required section order:

1. `# YYYY-MM-DD 早报/晚报`
2. Metadata lines:
   - `报告窗口：` with readable Chinese date/time, using same-day `08:30-20:30` or cross-day `至` format, and `（北京时间）`.
   - `收录文章：X 篇；来源公众号：Y 个`.
   - `引用说明：文中方括号数字对应文末“参考文献”。`
   Do not render `生成时间`, `新增文章：`, or public disclaimers.
3. `## 要点速览`: Markdown table with `主题 | 摘要 | 来源`.
4. `## 摘要速读`: one subsection per detail, each with cited evidence bullets. Do not insert generic theme-opening paragraphs such as `本组文章的主线是...`, `需要分开看...`, `不替代交易结论`, or `下方逐篇列出代表文章主旨`; if the evidence bullets already carry the information, omit the paragraph.
5. `## 参考文献`: numeric reference entries with original links, formatted as `[1] 公众号名. 文章标题[EB/OL]. 微信公众号. 原文链接`. Do not append publish timestamps in this public reference list.

Do not render `## 信息边界` in the final Markdown report. Keep generation limits, source-level warnings, secondary-only evidence, duplicate-source notes, and empty/body-missing warnings in `quality_warnings_json` and optional `source_audit_json` for internal review.

If a public evidence point intentionally keeps an exact original sentence, render it as a Markdown blockquote with its numeric citation label, for example `> 原句。 [1]`. Otherwise use a formal paraphrase.

## Prohibited Output

Do not generate action-oriented investment language:

- `投资建议`
- `投资影响`
- `投资机会`
- `推荐`
- `推荐：`
- `买入`
- `卖出`
- `关注方向`
- `配置建议`
- `受益：`
- `受益标的`
- `价值重估`
- `目标价`

Do not generate over-generalized sample claims:

- `核心变化`
- `趋势`
- `行业格局`
- `格局变化`
- `商业化叙事`
- `产业链支撑`

Do not generate empty analytical templates:

- `判断依据在于`
- `是否支撑`
- `这些信息支持的结论限于`
- `关键证据在于`
- `数字、日期和具体事实以证据句`

Do not generate colloquial, emotional, or headline-like wording:

- `狂烧`
- `这才`
- `啥`
- `一项项`
- `比如，我`
- `我一查`
- `我本来顺手`
- `为几个数字较真`
- `试探性激将`
- `过程就不展示`
- `并且当然`
- `触目惊心`
- `一次性垃圾`
- `自个儿`
- `不限量`
- `……`
- `？`

Source titles may contain finance terms, but generated prose must stay descriptive.

Do not expose low-signal metadata or crawler/source notes as article summaries:

- `公开发表于`
- `原始内容参考`
- `内容提要`
- `报告文章摘要概述`
- `文章摘要概述`
- `投资逻辑`
- `导语`
- `今日好文`
- `原文正面表述`
- `疼痛线`
- YouTube or other raw URL boilerplate unless the URL itself is the fact being discussed.

Do not produce direction-only article bullets when the body has richer facts. For example, replace `在访谈中讨论英特尔代工、产品路线和长期回报目标` with the actual cooperation party, capital action, technology route, and target found in the body.

## Theme Classification

- Use the article's main object and action as the classification basis: model/platform capability, hardware component/material, compute infrastructure, software engineering/data infrastructure, policy/security event, robotics, or finance/company event.
- Broad business or risk words such as `市场`, `价格`, `融资`, `估值`, `营收`, `亏损`, `安全`, and `风险` are secondary evidence. They are not enough to override strong domain anchors such as `OpenRouter`, `Fable`, `Fusion`, `Claude`, `GLM`, `光纤`, `MLCC`, `HBM`, `GPU`, `TPU`, `Kafka`, or `Agent`.
- Use `金融市场与公司经营` when the article's main subject is macro rates/data, financial statements, funding rounds, valuation, IPO, asset pricing, or company operating results. Do not use it as a catch-all bucket for every article containing a number, price, cost, or financing detail.

Do not generate low-information briefing templates:

- `XX主题下`
- `文章集中讨论`
- `共同线索是`
- `共同指向`
- `本时段核心不是单篇消息本身`
- `从来源分布看`
- `可比的信息不是标题热度`

These phrases are too generic for the report module. Replace them with a direct statement of what the referenced articles show, why it matters inside the evidence boundary, and which constraint or factual relationship is supported by the source text.

## Window Semantics

- `window_start` and `window_end` are fixed slot boundaries in Asia/Shanghai. Report membership is based on WeRSS `articles.publish_time` converted to those boundaries.
- `created_at` and `updated_at` are crawler/database record times. They may be displayed or audited as fetch metadata, but they must not decide whether an article belongs to a report window.
- `generated_at` records when the report was actually produced and may be later than `window_end`.
