#!/usr/bin/env python3
"""validate_report.py — pre-delivery lint for vibe-coding-review reports.

Usage: validate_report.py <report.md>

Exit 0 = pass (warnings allowed), exit 1 = errors that must be fixed before
delivering the report. Stdlib only, no dependencies.

Checks (schema_version 2):
  - frontmatter present and parseable (simple key/list parsing)
  - required keys per review_type; score_snapshot has 6 integer values 1-10
  - filename format, and the topic segment is not the bare generic "阶段复盘"
  - tag hygiene: kebab-case, no status suffixes (-improved/-fixed/-resolved)
  - required sections per review_type (TL;DR, merged chapters)
  - content length budget (chars, excluding frontmatter)
"""
import re
import sys
import unicodedata
from pathlib import Path

SCORE_KEYS = [
    "project_clarity",
    "architecture_understanding",
    "ai_direction_quality",
    "product_judgment_quality",
    "validation_awareness",
    "compounding_quality",
]

REQUIRED_KEYS_COMMON = ["type", "schema_version", "project", "review_type", "created", "scope", "tags"]
REQUIRED_KEYS_STAGE = REQUIRED_KEYS_COMMON + [
    "source_repo", "baseline_commit", "head_commit",
    "review_issue_tags", "prompt_constraint_tags", "score_snapshot",
]
REQUIRED_KEYS_MONTHLY = REQUIRED_KEYS_COMMON + ["included_reports", "aggregated_issue_tags"]

SECTIONS_STAGE = [
    "## TL;DR",
    "## 1. 本阶段做了什么",
    "## 2. 推进流程与 AI 指挥",
    "## 3. 架构理解",
    "## 4. 本阶段词典",
    "## 5. 产品判断",
    "## 6. Debug 与返工",
    "## 7. 评分卡与趋势",
    "## 8. 问题、标签与下次约束",
    "## 附录：证据盘点",
]
SECTIONS_FINAL = [
    "## TL;DR",
    "## 7. 评分卡与趋势",
    "## 8. 问题、标签与下次约束",
    "## 附录：证据盘点",
]

LENGTH_BUDGET = {"阶段复盘": (12000, 15000), "完整复盘": (24000, 30000), "月度复盘汇总": (16000, 20000)}

BAD_TAG_SUFFIXES = ("-improved", "-fixed", "-resolved", "-blocked", "-done")
TAG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FILENAME_STAGE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}__[^_]+.*__(.+)\.md$")
FILENAME_MONTHLY_RE = re.compile(r"^\d{4}-\d{2}__.+__月度复盘汇总\.md$")


def parse_frontmatter(text):
    """Minimal YAML-ish parser: top-level `key: value` and `key:` + `  - item` lists
    and one nested level for score_snapshot. Returns (dict, content_after)."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    body = text[4:end]
    content = text[end + 5:]
    data = {}
    current_list = None
    current_map = None
    for line in body.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_list is not None:
            data[current_list].append(line[4:].strip())
        elif re.match(r"^  [A-Za-z_]+:", line) and current_map is not None:
            k, _, v = line.strip().partition(":")
            data[current_map][k.strip()] = v.strip()
        elif re.match(r"^[A-Za-z_]+:", line):
            k, _, v = line.partition(":")
            k, v = k.strip(), v.strip()
            current_list = current_map = None
            if v == "":
                if k == "score_snapshot":
                    data[k] = {}
                    current_map = k
                else:
                    data[k] = []
                    current_list = k
            else:
                data[k] = v
    return data, content


def main():
    if len(sys.argv) != 2:
        print("usage: validate_report.py <report.md>", file=sys.stderr)
        return 1
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ERROR: file not found: {path}")
        return 1
    text = path.read_text(encoding="utf-8")
    errors, warnings = [], []

    fm, content = parse_frontmatter(text)
    if fm is None:
        print("ERROR: no parseable frontmatter (must start with ---)")
        return 1

    review_type = fm.get("review_type", "")
    if review_type not in ("阶段复盘", "完整复盘", "月度复盘汇总"):
        errors.append(f"review_type must be 阶段复盘/完整复盘/月度复盘汇总, got: {review_type!r}")

    required = REQUIRED_KEYS_MONTHLY if review_type == "月度复盘汇总" else REQUIRED_KEYS_STAGE
    for k in required:
        if k not in fm:
            errors.append(f"frontmatter missing required key: {k}")

    if str(fm.get("schema_version", "")) != "2":
        errors.append(f"schema_version must be 2, got: {fm.get('schema_version')!r}")

    # score_snapshot: 6 integers 1-10 (null allowed with warning) for stage/final
    if review_type in ("阶段复盘", "完整复盘") and isinstance(fm.get("score_snapshot"), dict):
        snap = fm["score_snapshot"]
        for k in SCORE_KEYS:
            v = snap.get(k)
            if v is None:
                errors.append(f"score_snapshot missing key: {k}")
            elif v == "null":
                warnings.append(f"score_snapshot.{k} is null — only allowed when truly undeterminable")
            elif not (v.isdigit() and 1 <= int(v) <= 10):
                errors.append(f"score_snapshot.{k} must be integer 1-10, got: {v!r}")

    # tag hygiene
    for field in ("review_issue_tags", "prompt_constraint_tags", "aggregated_issue_tags"):
        for tag in fm.get(field, []) if isinstance(fm.get(field), list) else []:
            if tag == "tag-or-none":
                continue
            if not TAG_RE.match(tag):
                errors.append(f"{field}: tag not kebab-case: {tag!r}")
            if tag.endswith(BAD_TAG_SUFFIXES):
                errors.append(f"{field}: status suffix forbidden in tag (progress belongs in 评分趋势): {tag!r}")

    # filename
    name = path.name
    if review_type == "月度复盘汇总":
        if not FILENAME_MONTHLY_RE.match(name):
            errors.append(f"filename must match YYYY-MM__项目名__月度复盘汇总.md, got: {name}")
    elif review_type in ("阶段复盘", "完整复盘"):
        m = FILENAME_STAGE_RE.match(name)
        if not m:
            errors.append(f"filename must match YYYY-MM-DD_HH-mm__项目名__主题.md, got: {name}")
        else:
            topic = m.group(1)
            # 完整复盘 filenames legitimately end in __完整复盘.md; only the stage
            # type forbids the bare generic topic.
            if review_type == "阶段复盘" and topic in ("阶段复盘", "完整复盘"):
                errors.append(
                    f"filename topic segment is the bare generic {topic!r} — must contain the stage code/theme, "
                    "e.g. 阶段8.3_桌面数据与密钥边界复盘"
                )

    # required sections
    if review_type == "阶段复盘":
        for s in SECTIONS_STAGE:
            if s not in content:
                errors.append(f"missing required section: {s}")
    elif review_type == "完整复盘":
        for s in SECTIONS_FINAL:
            if s not in content:
                errors.append(f"missing required section: {s}")

    # TL;DR must be 3 bullet lines near the top
    if review_type in ("阶段复盘", "完整复盘") and "## TL;DR" in content:
        tldr = content.split("## TL;DR", 1)[1].split("##", 1)[0]
        bullets = [l for l in tldr.splitlines() if l.strip().startswith("- ")]
        if len(bullets) != 3:
            errors.append(f"TL;DR must contain exactly 3 bullet lines, got {len(bullets)}")

    # length budget (content only, excluding frontmatter)
    if review_type in LENGTH_BUDGET:
        soft, hard = LENGTH_BUDGET[review_type]
        n = len(content)
        if n > hard:
            errors.append(f"content length {n} chars exceeds hard budget {hard} for {review_type} — cut, do not append")
        elif n > soft:
            warnings.append(f"content length {n} chars exceeds soft budget {soft} for {review_type}")

    # table row sanity: header/separator/data cell-count mismatch (catches silent cell loss)
    def cell_count(row):
        return row.strip().replace("\\|", "").strip("|").count("|") + 1

    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            ncols = cell_count(line)
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                if cell_count(lines[j]) > ncols:
                    errors.append(f"line {j + 1}: table row has {cell_count(lines[j])} cells but header has {ncols} — extra cells render silently lost")
                j += 1

    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s) — fix and re-run before delivering the report.")
        return 1
    print(f"PASSED: 0 errors, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
