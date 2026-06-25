# D91 Integration Notes

The briefing belongs to the website module, not the Feishu daily report project.

## Backend

- Keep the API path `/v1/mp/reports`.
- Keep the table `mp_article_reports`; add compatible nullable columns for structured report fields.
- Read WeRSS SQLite from configured `WERSS_DB_PATH`.
- Use `articles.publish_time` for report window inclusion.
- Keep `window_end` fixed to the report slot cutoff (`08:30` or `20:30`); never extend the report because generation ran later.
- Write Markdown to `MP_REPORT_ARCHIVE_ROOT`.
- Return structured JSON fields for frontend rendering; do not ask the frontend to parse Markdown.

## Frontend

- Keep `/mp` as the entry route.
- Render report data with native React components.
- Make source links open original WeChat URLs in a new tab.
