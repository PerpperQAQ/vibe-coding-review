# Execution Examples

Execution guidance for trigger decisions, lookup, tags, and validation. Not report sections.

## Example 1: Single-window stage review

```text
使用 $vibe-coding-review 给这个项目做一次个人阶段复盘。
范围：最近 3 次 commit 和当前窗口完整上下文。
```

Expected behavior:

- Use `阶段复盘`; read current-window context first, then repository evidence inside the stated scope.
- Do not search historical sessions or background threads.
- Run `scripts/find_previous.sh <review_dir> <source_repo>` before the scoring table; fill "上次" from its output.
- Run `scripts/find_previous.sh <review_dir> <source_repo> --tags` before writing `review_issue_tags`; reuse existing tags.
- Run `scripts/validate_report.py` on the written file; fix errors and re-run.

## Example 2: Claiming "no previous report"

Only allowed like this:

```text
$ scripts/find_previous.sh "<review_dir>" /path/to/repo
# 0 report(s) match source_repo: /path/to/repo
# NO matching previous report. ...
```

Quote the zero-match line in §7. If the script lists reports, the newest one is the baseline — even when the project's display name changed (matching is by `source_repo`, not filename).

## Example 3: New tag justification

The stage exposed a problem not covered by references/tag-vocabulary.md or `--tags` output. In §8:

```text
- 标签：live2d-asset-spec-drift
  新标签理由：现有标签 evidence-boundary-gap 描述的是证据边界，本问题是资产规格与模型能力不匹配，词表无对应家族。
```

Without that line, reuse the closest existing tag instead.

## Example 4: Multi-window evidence (opt-in only)

```text
使用 $vibe-coding-review 做一次个人阶段复盘。
本阶段跨了两个窗口，导出记录在 exports/stage-8-planning.md 和 exports/stage-8-impl.md。
```

Expected behavior:

- Read only the two provided files as multi-window evidence; record them in the appendix evidence table.
- Never scan Codex sessions / Claude Code transcripts / other tool histories uninvited.
- If a provided path is missing, record it under 证据边界 and continue.

## Example 5: Non-trigger

```text
给这个项目写一份 changelog，总结最近发布了什么。
```

Do not use this skill — project documentation, not a personal learning review.

## Example 6: Monthly summary

```text
使用 $vibe-coding-review 基于 2026-07 的复盘报告生成月度复盘汇总。
```

Expected behavior:

- Use `月度复盘汇总`; inputs are the reports, not the repository.
- Use `find_previous.sh --tags` frequency output as the basis of the tag-trend table.
- For each top tag, judge whether last month's 阻断动作 took effect before prescribing a new one.
