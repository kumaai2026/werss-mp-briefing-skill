# D91 Integration Notes

The briefing belongs to the website module, not the Feishu daily report project.

## Backend

- Keep the API path `/v1/mp/reports`.
- Keep the table `mp_article_reports`; add compatible nullable columns for structured report fields.
- Read WeRSS SQLite from configured `WERSS_DB_PATH`.
- Use `articles.publish_time` for window inclusion. It is the original article time stored as Unix seconds and must be compared against fixed Asia/Shanghai slot cutoffs.
- Use `created_at` and `updated_at` only as crawler/database record metadata.
- Classify report themes by the article's primary subject and domain anchors. Broad business or risk words such as prices, market size, funding, valuation, revenue, losses, safety, or risk should not override explicit AI model, semiconductor hardware, compute infrastructure, software engineering, policy, market-record, or robotics anchors.
- Keep `window_end` fixed to the report slot cutoff (`08:30` or `20:30`); never extend the report because generation ran later.
- Write Markdown to `MP_REPORT_ARCHIVE_ROOT`.
- Return structured JSON fields for frontend rendering; do not ask the frontend to parse Markdown.

## Frontend

- Keep `/mp` as the entry route.
- Render report data with native React components:
  - report metadata band
  - key-points table on desktop
  - stacked cards on mobile
  - expandable detail sections
  - source links
  - quality warnings
- Avoid nested UI cards; this is a work dashboard, so use dense, readable sections.
- Make source links open original WeChat URLs in a new tab. Public source lists should use `参考文献` and numeric labels such as `[1] 公众号名. 文章标题[EB/OL]. 微信公众号. 原文链接`; do not append publish timestamps in the public reference list. Internal `S1` ids may remain in JSON but must not be rendered publicly.

## Deployment

- Add a writable Docker mount for the Markdown archive root.
- Rebuild the API container after backend changes.
- Rebuild the frontend container after `/mp` UI changes.
- Verify via local `/api/v1/mp/reports?limit=1`, local `/mp`, and `Host: kuma.d91.global`.
