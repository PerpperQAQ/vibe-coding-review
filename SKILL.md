---
name: vibe-coding-review
description: Generate personal learning-oriented vibe coding review reports and monthly review summaries that turn AI-assisted coding projects into reusable learning assets. Use only when the user explicitly asks for personal复盘, vibe coding复盘, 学习复利, 项目负责人复盘, 个人成长总结, 评分卡, 改进问题分析, or 月度复盘汇总 from an AI-assisted coding project. Do not use for ordinary project-internal technical summaries, stage progress summaries, changelogs, release notes, implementation notes, handoff docs, README updates, or development status documents unless the user explicitly says the output is for their personal vibe-coding learning review.
---

# Vibe Coding Review

## Purpose

Act as an objective project review advisor for a non-programmer who builds software with AI coding tools (Codex, Claude Code, OpenCode, Cursor, Trae). Output is a single Chinese Markdown report for the user to read in Obsidian.

Learning value priority: 1) development process, 2) architecture understanding, 3) how the user directed AI, 4) product judgment, 5) code knowledge, 6) debug thinking. Do not turn the report into a line-by-line code tutorial.

## Trigger Boundary

Personal learning review only — never project documentation. Do not use for stage technical summaries, progress records, changelogs, implementation notes, handoff docs, README/docs updates, or sprint reports meant to live inside the project. When wording like "阶段性总结" is ambiguous, decide by audience: repository → do not use this skill; the user's personal learning (个人复盘, 学习复利, 给我自己看, scoring, improvement analysis) → use it.

## Output Location

Resolve the output directory in this order:

1. Directory explicitly provided by the user.
2. `.local/output-location.md` next to this SKILL.md (machine-local, never committed): first existing absolute path, or the value after `output_dir:` / `review_root:`.
3. Project-local `.vibe-coding-review/output-location.md`, same format.
4. Environment variable `VIBE_CODING_REVIEW_DIR`.
5. Auto-discover an existing review root (directories named `Vibe coding复盘`, `Vibe coding reviews`, or `vibe-coding-reviews` under `$HOME/Library/CloudStorage`, `$HOME/Documents`, `$HOME/Obsidian`, `$HOME/OneDrive*`, `$HOME/Dropbox`).
6. If none found, ask the user for a directory instead of writing a personal review into the repository.

First-run persistence: whenever the directory was resolved by step 4-5 (not by an explicit config), write the result into `.local/output-location.md` and tell the user — auto-discovery is a one-time bootstrap, not a per-session path. Prefer a per-project subdirectory under the review root. Create the directory if missing.

Filenames (project name filesystem-safe; use the user's timezone):

- `YYYY-MM-DD_HH-mm__项目名__阶段N_主题复盘.md` — the topic segment must contain the concrete stage code/theme; the bare word `阶段复盘` is forbidden and fails validation.
- `YYYY-MM-DD_HH-mm__项目名__完整复盘.md`
- `YYYY-MM__项目名__月度复盘汇总.md`

No decorative prefixes (⭐️ etc.) in the project segment — importance markers belong in frontmatter tags.

## Review Types

- `阶段复盘`: a completed feature, iteration, debugging or deployment milestone.
- `完整复盘`: project complete, delivered, paused, or user asks for a full review.
- `月度复盘汇总`: aggregate multiple existing reports; compare scores, repeated tags, trends.

Infer from wording; default to `阶段复盘` and state the assumption.

## Scope And Previous-Report Lookup

Use the scope the user gives (commits, branch, feature, date range). Without one: baseline = previous report's `head_commit`, else its `created` time, else visible history with the evidence boundary marked.

Previous-report lookup is script-driven, never improvised:

- Run `scripts/find_previous.sh <review_dir> <source_repo> [count]`, where `<review_dir>` is the per-project review directory reports are written into. Matching key is the frontmatter `source_repo` path — never the project name in filenames (display names change; the repo path is stable).
- The trend table's "上次" column comes from this output. Claiming "暂无上一份可比较报告" is only allowed after the script printed its zero-match line; quote that line in the report.
- Before writing `review_issue_tags`, run `scripts/find_previous.sh <review_dir> <source_repo> --tags` for the reuse-first check (see Tags).

## Evidence Rules

- For 阶段复盘/完整复盘, the current-window conversation is first-class evidence: original goal, prompt constraints, scope changes, AI decisions, tool/test outputs, validation, unresolved blockers. Never summarize only the final diff when window context is available; never use final commits or success messages as substitutes for process or acceptance evidence.
- Multi-window evidence is strictly opt-in: only read exported transcripts, summary files, or paths the user explicitly provides. Never scan session histories on your own.
- Record everything unavailable, truncated, or out-of-scope under 证据边界 in the appendix. Never fabricate chat history, tests, deployments, or intent; mark inferences as inferences.
- For 月度复盘汇总, the input is the reports themselves, not the repository.
- Prefer `rg` for searching, git for history/diffs.

## Frontmatter (schema_version: 2)

Every report — including any project-wide overview the user requests through this skill — carries full frontmatter. Required keys for 阶段复盘/完整复盘:

```yaml
type: vibe-coding-review
schema_version: 2
project: 项目名
review_type: 阶段复盘
created: YYYY-MM-DD HH:mm
source_repo: /absolute/path/to/repo
scope: 简短范围说明
baseline_commit: commit-or-null
head_commit: commit-or-null
tags: [vibe-coding, project-review, learning-compound]
review_issue_tags: [tag-or-none]
prompt_constraint_tags: [tag-or-none]
score_snapshot:
  project_clarity: null
  architecture_understanding: null
  ai_direction_quality: null
  product_judgment_quality: null
  validation_awareness: null
  compounding_quality: null
```

`score_snapshot` holds the same integers as the report's scoring table (null only when truly undeterminable). 月度复盘汇总 replaces `score_snapshot`/`review_issue_tags` with `included_reports` and `aggregated_issue_tags`, and sets `source_repo: null` unless one repo is clearly relevant. Do not invent extra frontmatter keys.

## Scoring

Six fixed dimensions, 1-10 each: 项目推进清晰度, 架构理解程度, AI 指挥质量, 产品判断质量, 验收与测试意识, 复利沉淀质量.

Anchors — scores reflect evidence, not encouragement:

- 10 = a project-owner behavior appeared this stage that had never been done before, with concrete evidence. Maintaining an existing habit is capped at 9.
- 9 = existing high standard maintained, no new behavior.
- 7-8 = mostly done with a named gap.
- 5-6 = a real failure in this dimension this stage.
- ≤4 = the dimension was systematically absent.

Hard rules:

- A dimension cannot score 10 while `review_issue_tags` contains a tag whose 关联评分维度 (see references/tag-vocabulary.md) is that dimension — cap it at 9.
- Every score reason must cite one concrete behavior or quote from this stage. No behavior citation → no score above 8.
- The scoring table includes the "上次" column filled from `find_previous.sh` output; explain trend as behavior change, not numbers.

## Tags

Follow references/tag-vocabulary.md strictly: reuse-first (check `--tags` output), new tags need a one-line justification in §8, no status suffixes (-improved/-fixed), no praise entries in `review_issue_tags`, no stage-one-off task descriptions as tags. `prompt_constraint_tags` only holds constraint patterns reusable across stages.

## Report Structure

Templates live in references/report-templates.md — use the matching one. 阶段复盘 sections (all required):

- `## TL;DR` — exactly 3 bullets: 最重要的一个教训 / 明天要做的一个动作 / 下次提示词必加的一条约束.
- `## 1. 本阶段做了什么` — includes the stage's position in the project as one sentence.
- `## 2. 推进流程与 AI 指挥` — process table + direction-quality judgment.
- `## 3. 架构理解` — module table, one-sentence architecture change, user-action-to-response flow.
- `## 4. 本阶段词典` — ≤6 entries, project-contextual, keep the "你应该能复述成什么" column.
- `## 5. 产品判断` — conditional: expand only when a real product decision/validation happened this stage; otherwise one line referencing the previous conclusion.
- `## 6. Debug 与返工`
- `## 7. 评分卡与趋势` — one merged table (上次/本次/趋势/理由/改进方向).
- `## 8. 问题、标签与下次约束` — ≤3 problems, each written once: 问题/证据/影响/标签(+上次状态)/阻断动作/下次提示词片段. Optional 1-3 行动作业 at the end.
- `## 附录：证据盘点` — single table ≤8 rows + 范围/基线/证据边界.

A lesson appears in exactly one section — never restate the same point across §2/§7/§8.

Writing rules: Chinese unless asked otherwise; objective project-owner tone, direct but not harsh; separate observations from inferences; English terms get a Chinese gloss on first use (≤10 unglossed terms per report); short paragraphs, no raw terminal dumps; no absolute local paths in reusable prompt fragments.

Length budgets (content excluding frontmatter, enforced by validator): 阶段复盘 soft 12k / hard 15k chars; 完整复盘 24k/30k; 月度复盘汇总 16k/20k. Over budget → cut, never append.

## Validation (mandatory final step)

Before delivering any report, run:

```
python3 scripts/validate_report.py <report-file>
```

Fix every ERROR and re-run until it passes; mention remaining WARNs to the user. After finishing a 阶段复盘, if `find_previous.sh` shows ≥8 same-project reports since the last 月度复盘汇总, append one suggestion line to your chat reply (not the report) recommending a monthly summary and naming the top repeated tags.
