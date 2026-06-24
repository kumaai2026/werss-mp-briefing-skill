# Output Contract

Use these JSON fields for D91 website rendering.

## summary_table_json

Array of objects:

- `theme`: short factual topic name, preferably from article title/body terms.
- `core_viewpoint`: concise summary content for the table cell. It may contain 3-8 short points for the theme, separated in Markdown/HTML rendering as line breaks. Merge similar viewpoints, remove repeated wording, preserve newly added information, and use concise declarative sentences.
- `sources`: array of pure numeric source ids as strings, such as `["1", "3"]`.

## details_json

Array of objects:

- `theme`: same topic name used in the table when possible.
- `summary`: objective synthesis from referenced article bodies, explaining the shared logic, differences, and evidence boundary. It must not be a stitched paragraph of raw source excerpts or a generic setup paragraph.
- `evidence_points`: array of `{ "text": "...", "sources": ["1"] }`.
- `sources`: unique source ids used by this detail section.

## sources_json

Array of objects:

- `id`: pure numeric source id as a string, such as `1`, `2`, ...
- `article_key`
- `title`
- `account_name`
- `publish_time`
- `fetched_at`
- `url`
- `section_label`
- `evidence_text`: trimmed text used only for validation/debugging. The website may omit or hide it.

## report_markdown

Required section order:

1. `# YYYY-MM-DD 早报/晚报`
2. Metadata lines: report window, generated time, article count, account count.
3. `## 要点速览`: Markdown table with `主题 | 摘要 | 来源`. Keep this table format; summary-content rules apply inside the `摘要` cell.
4. `## 摘要速读`: one subsection per detail, each with cited evidence bullets.
5. `## 引用来源`: source ids with original links.

Citation display rules:

- Keep JSON source ids pure numeric strings.
- In Markdown prose and tables, display source ids with corner brackets, such as `「1」`.
- In the `来源` column, each displayed citation number must be a Markdown link to the original article URL, such as `[「1」](https://...)`.
- When multiple sources support one row, render each source number as its own original-article link, separated by `、`.

## Prohibited Output


## Window Semantics

- `window_start` and `window_end` are fixed slot boundaries based on WeRSS `articles.published_at`.
- `generated_at` records when the report was actually produced and may be later than `window_end`.
