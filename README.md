# vibe-coding-review

`vibe-coding-review` is a Codex skill for people who build projects with AI coding tools and want each project to become a reusable learning asset.

It turns AI-assisted development evidence such as code changes, plans, chat decisions, logs, validation results, and existing review reports into structured Markdown reviews. The reports are designed to be read in Obsidian or any Markdown editor.

## Why This Exists

Vibe coding can help a non-programmer ship projects quickly, but it often leaves one problem unsolved: after the project is done, the human still may not understand the development process, architecture, product decisions, or how to direct AI better next time.

This skill is built to close that loop. It acts like an objective project review advisor. It does not merely summarize files. It helps the user understand:

- what happened during the project
- how the project moved from idea to implementation
- how the architecture is organized
- how the user directed AI
- where product or business judgment is weak
- what should be reused or changed in the next project

## Review Modes

### Stage Review

Use this after a feature, iteration, debugging milestone, deployment milestone, or other partial project milestone.

Stage reviews prioritize evidence inside the requested scope:

- diffs
- implementation plans
- chat decisions
- error logs
- validation or acceptance results

### Final Project Review

Use this when a project is complete, delivered, paused, or ready for a full retrospective.

Final reviews expand to the whole project and analyze architecture, major decisions, product maturity, business landing readiness, repeated problems, and reusable lessons.

### Monthly Review Summary

Use this across multiple existing review reports.

Monthly summaries compare score changes, repeated problems, unfinished homework, and whether the user is improving as a project owner.

## Installation

Clone this repository into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone <REPO_URL> ~/.codex/skills/vibe-coding-review
```

Restart Codex or reload skills if your environment requires it.

## Output Directory

The skill does not hard-code the original creator's local paths.

It chooses the report output directory in this order:

1. A directory explicitly provided in your request.
2. The `VIBE_CODING_REVIEW_DIR` environment variable.
3. A project-local review directory such as `docs/vibe-coding-reviews`, `notes/vibe-coding-reviews`, or `reviews/vibe-coding-reviews`.
4. `vibe-coding-reviews/` in the current project root.

For Obsidian, set `VIBE_CODING_REVIEW_DIR` to a folder inside your vault:

```bash
export VIBE_CODING_REVIEW_DIR="$HOME/Documents/Obsidian/Vibe coding reviews"
```

You can also tell Codex the output folder directly in your prompt.

## Usage

Stage review:

```text
Use $vibe-coding-review to generate a stage review for this project.
Scope: the last 3 commits.
Save it to my Obsidian review folder.
```

Final project review:

```text
Use $vibe-coding-review to generate a final project review for this project.
Focus on development process, architecture, AI direction, product maturity, and reusable lessons.
```

Monthly summary:

```text
Use $vibe-coding-review to generate a monthly review summary from these review reports.
Compare score changes, repeated problems, and unfinished action homework.
```

## Report Focus

The skill prioritizes learning value in this order:

1. Project development process
2. Architecture understanding
3. How the user directed AI
4. Product or business judgment
5. Code knowledge
6. Debug thinking

It intentionally avoids becoming a line-by-line code tutorial. Code is explained only when it helps the user understand the project, architecture, workflow, or decision quality.

## Safety And Privacy

Before publishing or sharing generated reviews, inspect them for private information. Project reviews may include:

- local file paths
- chat excerpts
- commit messages
- deployment URLs
- product ideas
- business assumptions
- error logs
- screenshots or PR references

The skill instructions tell Codex not to fabricate missing evidence and not to hard-code creator-specific paths.

## Repository Contents

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    └── report-templates.md
```

## Validation

If you have the Codex skill creator scripts available, validate the skill with:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py ~/.codex/skills/vibe-coding-review
```
