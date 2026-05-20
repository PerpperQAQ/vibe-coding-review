---
name: vibe-coding-review
description: Generate personal learning-oriented vibe coding review reports and monthly review summaries that turn AI-assisted coding projects into reusable learning assets. Use only when the user explicitly asks for personal复盘, vibe coding复盘, 学习复利, 项目负责人复盘, 个人成长总结, 评分卡, 改进问题分析, or 月度复盘汇总 from an AI-assisted coding project. Do not use for ordinary project-internal technical summaries, stage progress summaries, changelogs, release notes, implementation notes, handoff docs, README updates, or development status documents unless the user explicitly says the output is for their personal vibe-coding learning review.
---

# Vibe Coding Review

## Purpose

Use this skill to act as an objective project review advisor for a non-programmer who builds software with AI coding tools such as Cursor, Trae, Codex, and Claude Code. The output is a single Markdown report for the current user to read in Obsidian.

Prioritize learning value in this order:

1. Project development process
2. Architecture understanding
3. How the user directed AI
4. Product or business judgment
5. Code knowledge
6. Debug thinking

Do not turn the report into a line-by-line code tutorial. Explain code only when it helps the user understand the project, architecture, workflow, or decision quality.

## Trigger Boundary

Use this skill only for the user's personal learning review, not for normal project documentation.

Do not use this skill for:

- Project-internal stage technical summaries
- Development progress records
- Changelogs or release notes
- Implementation notes
- Handoff documents for other developers or agents
- README or docs updates
- Sprint/status reports meant to live inside the project

When the user asks for "阶段性总结", "技术总结", "开发进度总结", "阶段文档", or similar wording, first decide whether the audience is the project or the user's personal learning. If the output is meant to record project progress inside the repository, do not use this skill. If the user explicitly says "个人复盘", "vibe coding 复盘", "学习复利", "给我自己看", "项目负责人复盘", or asks for scoring and personal improvement analysis, use this skill.

## Output Location

Choose the report output directory in this order:

1. Use the directory explicitly provided by the user.
2. If the environment variable `VIBE_CODING_REVIEW_DIR` is set, use that directory.
3. If the project has an existing `docs/`, `notes/`, or `reviews/` directory, create or use `docs/vibe-coding-reviews`, `notes/vibe-coding-reviews`, or `reviews/vibe-coding-reviews` in that order.
4. Otherwise, create `vibe-coding-reviews/` in the current project root.

For Obsidian users, recommend setting `VIBE_CODING_REVIEW_DIR` to a folder inside their vault or telling Codex the desired vault folder in the request. Do not hard-code the original creator's local paths or any user-specific path into generated reports.

Create the chosen directory if it does not exist.

Use this filename format:

`YYYY-MM-DD_HH-mm__项目名__阶段复盘.md`

or:

`YYYY-MM-DD_HH-mm__项目名__完整复盘.md`

or:

`YYYY-MM__项目名__月度复盘汇总.md`

Use the user's timezone when available. If no timezone is available, use the system local time. Derive `项目名` from the user request first, then the repository root folder name. Keep the project name filesystem-safe by replacing `/`, `:`, and newline characters with `-`.

## Review Type

Support three review types:

- `阶段复盘`: Use for a completed feature, iteration, debugging milestone, deployment milestone, or any partial project review.
- `完整复盘`: Use when the project is complete, delivered, paused, launched, or the user asks for a full project review.
- `月度复盘汇总`: Use when the user provides or points to multiple existing review reports and asks for a monthly summary, trend comparison, repeated-problem analysis, score comparison, or cross-project learning summary.

If the user does not specify the type, infer from their wording. If still unclear, default to `阶段复盘` and state that assumption in the report.

## Scope Rules

Use the scope the user explicitly gives, such as a date range, feature name, branch, commit range, PR, deployment, or "最近 3 次 commit".

If the user does not specify a scope:

1. Find the newest previous review for the same project in the chosen output directory.
2. Prefer the previous report's `head_commit` frontmatter as the baseline.
3. If no commit baseline exists, use the previous report's `created` time as a date baseline.
4. If no previous report exists, analyze the visible project history and mark the evidence boundary clearly.

When a previous same-project review exists, also extract its scores, repeated issue tags, action homework, and prompt-optimization directions. Use them for trend comparison and repeated-problem analysis in the new report.

Always include the chosen scope and evidence limitations in the report. Do not pretend missing evidence was analyzed.

## Evidence Collection

Start every review with an evidence inventory. Search broadly, but keep the final report focused.

Use different evidence depth by review type:

- For `阶段复盘`, prioritize evidence inside the stated scope: diff, implementation plan, chat decisions, error logs, and validation or acceptance results. Use broader repository documents only to explain context.
- For `完整复盘`, expand to the whole project: repository structure, full commit history when useful, README/docs, architecture notes, issue/PR history, deployment evidence, screenshots, logs, and all available AI artifacts.
- For `月度复盘汇总`, prioritize the user-provided review reports. Extract scores, repeated problems, action homework, project stages, and unresolved issues from those reports. Only inspect source repositories when the reports are insufficient and the user has clearly made them available.

Collect these evidence types when available:

- Repository state: project root, branch, git status, recent commits, changed files, diffs for the review scope.
- Project documents: README, docs, AGENTS, CLAUDE, package files, environment examples, configuration, architecture notes.
- AI artifacts: plans, TODO files, task lists, generated implementation notes, review notes.
- Chat records: current conversation context when available, exported Cursor/Trae/Codex/Claude Code chats, or files whose names suggest chat, prompt, conversation, transcript, log, or history.
- Logs and failures: terminal logs, test logs, build logs, deployment logs, error screenshots, issue notes.
- Product evidence: requirements, screenshots, UI captures, prototypes, PRs, issues, release notes, deployment URLs.
- Existing review reports: prior `阶段复盘`, `完整复盘`, and monthly summaries supplied by the user or found in the output directory.

Prefer `rg` and `rg --files` for searching. Use git commands for history and diffs. Use `gh` only when a GitHub PR or issue is relevant and authentication is already available.

When chat records or other requested sources cannot be found automatically, record them under "缺失证据". Explain the impact briefly instead of asking the user to stop and provide them unless the review would be meaningless without them.

## Product And Business Analysis

Always adapt product and business analysis to the current development stage and actual project content. Do not write generic business advice.

- For an early project setup or first-stage review, emphasize feasibility analysis: target user clarity, problem validity, scope realism, technical feasibility, minimum viable path, and biggest unknowns.
- For normal stage reviews, emphasize commercialization and product completeness for the current stage: whether the feature moves the project closer to usable value, what product gaps remain, what user or revenue assumptions were strengthened or weakened, and what must be validated next.
- For final project reviews, emphasize complete product and business landing maturity: user value, market or usage scenario fit, monetization or distribution path if relevant, operational readiness, delivery quality, adoption risks, and next-step go/no-go judgment.
- For monthly summaries, compare how product judgment evolved across reports: repeated product blind spots, improving or worsening commercial clarity, and whether the user is accumulating better product-owner instincts.

If the evidence is insufficient for product or business judgment, state the limitation and make only bounded inferences.

## Monthly Summary Mode

When generating `月度复盘汇总`, read multiple review reports rather than re-reviewing a single codebase.

Required monthly summary behavior:

- Use the reports explicitly provided by the user. If the user gives a month and project but no files, search the chosen output directory for matching reports.
- List every included report with filename, review type, project, date, and whether scores were found.
- Compare the six fixed scoring dimensions over time. Use a table and identify upward, downward, and flat trends.
- Identify repeated problems from each report's "你这次真正需要改进的地方" chapter and from `review_issue_tags` when present.
- For repeated problems such as "the user keeps saying continue next stage", analyze the likely cause chain: visible behavior, evidence, why the behavior happens, how AI incentives amplify it, and what prompt or workflow constraint would interrupt it. Do not over-psychologize; tie the cause analysis to report evidence.
- Identify repeated or unfinished action homework.
- Summarize what the user appears to be learning across projects or stages.
- End with 1 to 3 monthly action homework items focused on changing the user's project-owner behavior.

Do not average scores mechanically without explaining what the trend means. If reports use missing or inconsistent scores, mark the comparison as incomplete.

## Report Writing Rules

Write in Chinese unless the user asks for another language.

Use a project-owner review style:

- Be objective and specific.
- Point out the user's problems directly, but do not add a deliberately harsh tone.
- Focus on decisions, process, scope control, validation, and AI direction.
- Explain architecture from the perspective of "how the project is organized and why".
- Keep code explanations shallow-to-deep: start with what a file/module does, then explain only the necessary mechanics.
- Separate observations from inferences. Mark uncertain claims as inference.
- Never fabricate chat history, business intent, tests, deployments, or architecture.

Make the Markdown clean in Obsidian:

- Include YAML frontmatter.
- Use clear `##` and `###` headings.
- Use tables for evidence inventory, scoring, and key module maps.
- Use short paragraphs and bullets.
- Use internal-friendly tags in frontmatter.
- Avoid raw terminal dumps; summarize important lines.
- Use fenced code blocks only for short commands, prompts, or snippets.

## Required Frontmatter

Every report must include:

```yaml
---
type: vibe-coding-review
project: 项目名
review_type: 阶段复盘
created: YYYY-MM-DD HH:mm
source_repo: /absolute/path/to/repo
scope: 简短范围说明
baseline_commit: commit-or-null
head_commit: commit-or-null
tags:
  - vibe-coding
  - project-review
  - learning-compound
---
```

For stage and complete reviews, also include structured metadata for future trend and monthly analysis:

```yaml
review_issue_tags:
  - tag-or-none
prompt_constraint_tags:
  - tag-or-none
score_snapshot:
  project_clarity: null
  architecture_understanding: null
  ai_direction_quality: null
  product_judgment_quality: null
  validation_awareness: null
  compounding_quality: null
```

Use short lowercase kebab-case values for tags, such as `continue-next-stage-inertia`, `vague-acceptance-criteria`, `missing-user-path-validation`, `weak-architecture-recall`, `overbroad-scope`, `static-tests-over-real-validation`, `unclear-product-gate`, or `unfinished-homework`. If no repeated issue is supported by evidence, use `tag-or-none`.

Fill `score_snapshot` with the same integer scores used in the report scoring table. Use `null` only when a score truly cannot be determined.

For complete reviews, set `review_type: 完整复盘`.

For monthly summaries, set `review_type: 月度复盘汇总`, set `source_repo: null` unless one project repository is clearly relevant, and use `included_reports` when helpful:

```yaml
included_reports:
  - report-file-name.md
```

## Scoring

Always include the fixed six scoring dimensions, each scored from 1 to 10:

- 项目推进清晰度
- 架构理解程度
- AI 指挥质量
- 产品判断质量
- 验收与测试意识
- 复利沉淀质量

For every score, include one concrete reason and one improvement direction. Scores should reflect evidence, not encouragement.

After the scoring table, include a score trend comparison when a previous same-project report is available. Compare the same six dimensions against the previous report, mark each as `上升`, `持平`, `下降`, or `无法比较`, and explain the behavior change behind the score movement. If no previous comparable report exists, explicitly say that this is the first comparable baseline.

## Core Concept Dictionary

For stage reviews, include a standalone chapter named:

`## 本阶段核心概念词典`

Explain 3 to 5 concepts that the user must understand to learn from this stage. These can be files, modules, architecture patterns, validation concepts, product concepts, or AI-collaboration concepts. Do not write generic textbook definitions. Explain each concept in the current project context:

- What it means in this project
- Why this stage needed it
- What the user should be able to say in their own words

Bias toward project understanding rather than programming vocabulary.

For complete reviews, use `## 项目核心概念词典` and select 5 to 8 concepts that explain the whole project.

## Improvement Chapter

Always include a standalone chapter named:

`## 你这次真正需要改进的地方`

Use this chapter to identify the user's most important process problems. Tie each problem to evidence, such as vague prompts, missing acceptance criteria, weak testing, unclear scope, over-reliance on AI continuation, or lack of architectural checkpoints.

## Repeated Issue Tags And Cause Analysis

For stage and complete reviews, include a standalone chapter named:

`## 重复问题标签与成因分析`

Tag the most important problems using stable kebab-case tags. Prefer reusing tags from previous reports for the same underlying behavior. For each tag, include:

- `本次是否出现`: 是/否/部分
- `证据`: where it appeared in prompts, commits, validation, docs, or missing evidence
- `成因判断`: why this behavior likely happens, based on evidence
- `AI 放大机制`: how AI tools may make the behavior easier to repeat
- `阻断动作`: one concrete prompt or workflow constraint for next time

When analyzing "continue next stage" behavior, distinguish at least these possible causes when evidence supports them: the user wants momentum, the stage goal is not written as an acceptance gate, AI fills missing scope by default, previous-stage documents create inertia, or the user lacks a quick product/architecture checklist before giving the next command.

## Action Homework

End with 1 to 3 small action homework items. Bias toward project understanding rather than generic programming study.

Good homework examples:

- Re-draw the module relationship map in your own words.
- Explain the request-to-render flow without looking at the report.
- Rewrite the original feature prompt with explicit acceptance criteria.
- Pick one key file and write a 5-line "what this file owns" note.

Avoid broad homework such as "learn React" or "study databases".

## Prompt Optimization Chapter

For stage reviews, do not end with a generic full prompt. Convert the problems found in `## 你这次真正需要改进的地方` into prompt-improvement directions.

The prompt optimization chapter must create a closed loop:

`observed problem -> prompt gap -> next constraint -> reusable prompt fragment`

Prefer 3 to 5 high-value directions. Tie each direction to an actual problem, score reason, debug issue, repeated issue tag, or acceptance gap from the report. Avoid broad reusable prompts that are not clearly derived from this review's evidence.

Classify each direction by prompt slot:

- `任务范围`: what this stage is and is not
- `验收标准`: what must be true before the stage counts as done
- `测试/证据要求`: what commands, screenshots, logs, or user-path checks must be shown
- `禁止事项`: what the AI must not expand into
- `handoff 要求`: what must be written for future agents or future stages
- `风险检查`: what similar-risk searches or edge cases must be checked
- `项目理解`: what the user must be able to explain back

Each reusable fragment must map back to one issue tag or one row in the prompt-gap table. Do not provide a polished all-purpose prompt unless the user explicitly asks for one.

## Templates

When generating the report, read `references/report-templates.md` and use the matching template:

- Use the stage template for `阶段复盘`.
- Use the final template for `完整复盘`.
- Use the monthly summary template for `月度复盘汇总`.

Adapt the template to available evidence, but keep the required chapters, scoring dimensions, improvement chapter, and action homework.
