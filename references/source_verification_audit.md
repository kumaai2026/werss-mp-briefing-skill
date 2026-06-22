# Source Verification Audit and Optimization Plan

## Scope

Input files reviewed on 2026-06-22:

- `/Users/kumaai/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_6bwbpd25rbwl12_e1c5/temp/drag/每日友商观点总结_2026年4月18-19日.pdf`
- `/Users/kumaai/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_6bwbpd25rbwl12_e1c5/temp/drag/每日自媒体资讯总结_20260419.pdf`

Method:

- Extracted PDF text with `pdftotext -layout`.
- Searched exact title/source phrases on the web.
- Opened primary or near-primary sources where discoverable.
- Checked the local WeRSS database at `/Users/kumaai/Documents/New project 2/werss/data/werss-data/db.db`. It starts at `2026-05-25`, so it cannot verify the April 2026 articles in these PDFs.

Status meanings:

- `supported`: original or primary source found and the summary is materially aligned.
- `partial`: source found, but the PDF wording overstates, compresses, or mixes source levels.
- `unverified`: exact original article/report was not found through web search or local WeRSS data.
- `conflict`: available source contradicts or materially weakens the PDF wording.

## Findings From The Two PDFs

### 每日友商观点总结

| Item | PDF source cue | Verification status | Comparison note |
| --- | --- | --- | --- |
| Web3 / tokenized securities | 国金证券电子团队, BlockBeats, SEC Rule 7.50 | partial | The SEC filing exists: Release No. 34-105260 / SR-NYSE-2026-17 says NYSE filed a proposed rule change to enable trading securities in tokenized form during a DTC pilot. The PDF should say NYSE filed and SEC published the notice, not that SEC itself "拟引入" the mechanism. |
| AI 链 Q1 业绩 | 国金证券电子团队 | unverified | Exact original research note was not found. Keep as secondary-source content unless the original report is available. |
| 北美算力租赁 | 国金证券计算机&科技团队 | unverified | Exact deep report was not found. Numbers and investment conclusions should not be promoted without source body. |
| 国产算力一芯 | 国联民生证券计算机团队 | unverified | Exact source was not found. |
| MiniMax 全球化 | 国金证券计算机&科技团队 | unverified | Exact source was not found. Company claims such as user count and geography need source body or official filing. |
| 三七互娱 | 浙商传媒互联网团队 | unverified | Exact note/company-announcement pairing was not found. |
| 光芯片 | 半导体行业观察 | partial | Underlying Marvell/Celestial reporting exists, but the PDF compresses deal economics and industry conclusions. Treat as article-derived unless the exact article is captured. |
| TGV / 光模块设备 | 中泰证券机械团队 | unverified | Exact source was not found. |
| 量子 AI | 招商证券计算机团队 | unverified | Exact source was not found. |
| 群核科技 | 国金证券传媒团队 | unverified | Exact source was not found. |
| 卫星互联网 | 招商证券计算机团队 | unverified | Exact source was not found. |

### 每日自媒体资讯总结

| Item | PDF source cue | Verification status | Comparison note |
| --- | --- | --- | --- |
| AI 云 IaaS 涨价 | 开源证券通信行业周报 | unverified | Exact report was not found. The Google Cloud Next date can be found in secondary event pages, but the PDF's pricing and recommendation claims need the actual research note. |
| Claude Code 桌面版 | InfoQ / Tina | unverified | Exact article and source-code metrics were not found. Treat as unverified. |
| MIA 记忆智能体 | arXiv 2604.04503, GitHub ECNU-SII/MIA | supported | The paper and repository exist. The PDF broadly matches the Manager-Planner-Executor, parametric/non-parametric memory, and test-time learning claims. It should preserve the paper's benchmark wording instead of mixing "7 datasets" with broader "11 benchmarks" language. |
| 高德 ABot 全栈具身技术 | 量子位 / 一水 | unverified | Exact article and primary ABot release were not found. |
| 高德 ABot-Claw | 新智元 / Aeneas | unverified | Exact article was not found. |
| 易鑫金融 Agent Harness | 新智元 / KingHZ | unverified | Exact article or primary talk transcript was not found. |
| Meta / Thinking Machines | Business Insider | supported | Business Insider reporting supports Joshua Gross joining Meta, the fifth founding-member framing, Soumith Chintala joining Thinking Machines, Neal Wu, valuation, and headcount context. The PDF adds rhetorical conclusions that are commentary, not source facts. |
| 伯克利 RDI 基准渗透 | 新智元 / 倾倾 | unverified | Exact source and "Bench Jack" references were not found. |
| MiniMax M2.7 Modified-MIT | AI 前线 / 华卫 | unverified | Exact source was not found. |
| 光芯片并购 | 半导体行业观察 | partial | WSJ and other sources support Marvell's Celestial AI deal, but the initial consideration is not the same as a simple "55 亿美元收购" statement; earnout terms should be separated. Other claims such as Nvidia 60 亿美元 locking capacity need direct sources. |
| ASML EUV / 内存 | 半导体行业观察, ASML Q1 2026 | partial | ASML's official Q1 2026 release supports Q1 sales, margin, net income, AI-driven demand, and memory/logic demand. The exact "内存 51% vs 逻辑 49%" split needs the original table or presentation evidence before being stated as a fact. |
| 三菱+罗姆+东芝功率半导体 | 半导体行业观察 / eetimes.jp | unverified | Exact source and figures were not found. |
| MacBook Neo A18 Pro | 9to5mac relay | partial | MacBook Neo and A18 Pro information is discoverable, but the exact supply-crisis article and "6-12 months" claim were not found. |
| OpenClaw 安全研究 | arXiv 2602.21127, HAT-Lab | partial | The paper supports 303 participants, 8.6% perception rate, HAT-Lab, six cognitive failure modes, and experiential learning. The OpenClaw-specific CVE / 512-vulnerability framing is not established by the paper itself and needs a separate primary security source. |
| OpenClaw 安全研究深度版 | arXiv 2602.21127, HAT-Lab | partial | Same as above. The repeated summary should be deduplicated rather than counted as two independent sources unless two separate articles are actually available. |

## Main Quality Problems Observed

1. Source labels are often not original-source links.
   Several rows cite a team/account name and date but not a retrievable URL or document id. The final summary reads as verified even when the original report was not found.

2. Secondary reports are mixed with primary evidence.
   Examples include SEC/NYSE filings, arXiv papers, ASML financial materials, and Business Insider reporting being summarized through a Chinese article without preserving source level.

3. Numeric claims need stronger grounding.
   Current validator checks generated numbers against `evidence_text`, but the source text itself may be a short digest. Important numbers should be traceable to article body or primary linked material.

4. Commentary is blended into facts.
   Phrases such as "人才奇点", "系统性吸血", "价值重估", "投资影响", and "受益" convert source facts into action-oriented or rhetorical conclusions.

5. Duplicate or derivative sources are not identified.
   The two OpenClaw sections appear to rely on the same paper and should not be treated as two independent confirmations.

6. Unverified originals are not surfaced to readers.
   The PDFs have no clear "原文不可核验 / 来源仅为二级摘要 / 关键数字未核验" boundary.

## Optimization Plan

### 1. Add a source verification pass before final writing

For every source article, classify:

- `body_verified`: WeRSS body exists and is long enough to support claims.
- `url_verified`: original URL opens or has been captured in WeRSS.
- `primary_link_verified`: article links to a paper, filing, company release, transcript, or data page and the link opens.
- `unverified`: only title/account/date or a short description is available.

The final report can still mention unverified sources, but core viewpoints should not rely on them without an internal `quality_warnings_json` or `source_audit_json` warning.

### 2. Compare final summaries against claim-level evidence

Before publishing, create a short claim audit for each `core_viewpoint`, `details.summary`, and `evidence_points` item:

- Claim text.
- Referenced source ids.
- Supporting source excerpt.
- Status: `supported`, `partial`, `unverified`, or `conflict`.
- Note when the claim is a synthesis rather than a direct source fact.

This can remain a debug/archive field and does not need to render on the website by default.

### 3. Separate primary and secondary sources

When an article cites a paper, filing, earnings release, or official transcript, add that primary URL to the source evidence notes. Do not collapse "Chinese article says X" and "primary source says X" into the same evidence level.

### 4. Tighten investment-language controls

Ban generated table headers or prose such as:

- `投资影响`
- `投资机会`
- `关注方向`
- `推荐：`
- `受益：`
- `受益标的`
- `价值重估`

If the source itself uses these terms, keep them only in source excerpts or source titles, not in generated analysis.

### 5. Add unresolved-source disclosure to internal quality fields

Every report should record internally:

- Number of sources with missing original body.
- Number of sources where only a secondary digest was available.
- Important claims or numbers excluded because the original was not verified.

Do not render these notes as a public `信息边界` section in the final Markdown report unless the user explicitly asks for a debug/audit view.

### 6. Keep implementation minimal

Recommended first implementation:

- Update the skill contract and output contract with the source-verification pass and optional `source_audit_json`.
- Extend `validate_report.py` to catch unknown source ids, detail-summary ungrounded numbers, and the additional action-oriented investment phrases.
- Do not change D91 `/mp` frontend/backend schema until real report payloads prove that `source_audit_json` should be persisted or rendered.

## Sources Opened During Audit

- SEC Release No. 34-105260 / SR-NYSE-2026-17: `https://www.sec.gov/files/rules/sro/nyse/2026/34-105260.pdf`
- MIA arXiv paper: `https://arxiv.org/abs/2604.04503`
- MIA GitHub repository: `https://github.com/ECNU-SII/MIA`
- HAT-Lab / AMD arXiv paper: `https://arxiv.org/abs/2602.21127`
- ASML Q1 2026 results: `https://www.asml.com/en/investors/financial-results/q1-2026`
- ASML Q1 2026 press release: `https://www.asml.com/en/news/press-releases/2026/q1-2026-financial-results`
- Business Insider Thinking Machines / Meta reporting: `https://www.businessinsider.com/thinking-machines-lab-loses-another-founding-member-to-meta-2026-4`
- WSJ Marvell / Celestial AI reporting: `https://www.wsj.com/business/marvell-technology-swings-to-profit-on-higher-data-center-demand-00cf6185`
