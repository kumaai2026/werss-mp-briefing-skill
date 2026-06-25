# Output Contract

Use these JSON fields for D91 website rendering.

## Top-level fields

- `title`: `YYYY-MM-DD 早报/晚报`
- `slot`: `morning` or `evening`
- `window_start`: fixed slot start based on original article publish time, formatted as `YYYY-MM-DD HH:MM`
- `window_end`: fixed slot end based on original article publish time, formatted as `YYYY-MM-DD HH:MM`
- `generated_at`: actual generation time, formatted as `YYYY-MM-DD HH:MM`
- `article_count`
- `account_count`
- `summary_table_json`
- `details_json`
- `sources_json`
- `report_markdown`

## summary_table_json

Array of objects:

- `theme`: short factual topic name, preferably from article title/body terms.
- `summary_points`: 3-8 concise point objects for the table cell, each as `{ "text": "...", "sources": ["1"] }`.
- `sources`: array of pure numeric source ids as strings, such as `["1", "3"]`.

## details_json

Array of objects:

- `theme`: same topic name used in the table when possible.
- `summary`: objective synthesis from referenced article bodies.
- `evidence_points`: array of `{ "text": "...", "sources": ["1"] }`.
- `sources`: unique source ids used by this detail section.

## sources_json

Array of objects:

- `id`: pure numeric source id as a string, such as `1`, `2`, ...
- `article_key`
- `title`
- `account_name`
- `publish_time`: display as `YYYY-MM-DD HH:MM`
- `fetched_at`: display as `YYYY-MM-DD HH:MM` when present
- `url`
- `section_label`
- `evidence_text`: trimmed source text for review/debugging. The website may omit or hide it.

## report_markdown

Required section order:

1. `# YYYY-MM-DD 早报/晚报`
2. Metadata lines: report window, generated time, article count, account count.
3. `## 要点速览`: Markdown table with `主题 | 摘要 | 来源`. Keep this table format; summary-content rules apply inside the `摘要` cell.
4. `## 摘要速读`: one subsection per detail, each with cited evidence bullets.
5. `## 引用来源`: ordered source list with original links.

Citation display rules:

- Keep JSON source ids pure numeric strings.
- In Markdown prose and tables, display source ids with corner brackets, such as `「1」`.
- In the `来源` column, each displayed citation number must be a Markdown link to the original article URL, such as `[「1」](https://...)`.
- When multiple sources support one row, render each source number as its own original-article link, separated by `、`.
- In `引用来源`, use normal ordered-list numbering and do not repeat corner-bracket source ids; display publish times as `YYYY-MM-DD HH:MM`.

## Window Semantics

- `window_start` and `window_end` are fixed slot boundaries based on the original article publish time (`articles.publish_time`).
- `generated_at` records when the report was actually produced and may be later than `window_end`; format it as `YYYY-MM-DD HH:MM`.
