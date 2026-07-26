# vibe-coding-review

`vibe-coding-review` 是一个可部署到 Codex、Claude Code、OpenCode 等 AI Coding 工具的 Skill，用来把 AI 辅助编程项目沉淀成可复用的个人学习复盘。

它不是普通项目总结器，也不是逐行讲代码的教程。它关注的是：项目是怎样被推进的、你如何指挥 AI、架构和验收哪里没想清楚、哪些问题正在重复出现，以及下一次项目应该怎样做得更好。

## v2 的变化（schema_version 2）

基于 91 份真实产出的全量审计，v2 把散文规则换成了确定性护栏：

- **脚本护栏**：`scripts/find_previous.sh` 按 frontmatter `source_repo` 查找同项目历史报告（项目改名不再断链），趋势表和"暂无可比较报告"都必须以它的输出为依据；`scripts/validate_report.py` 在交付前校验 frontmatter、文件名、章节、表格和长度预算。
- **受控标签词表**：`references/tag-vocabulary.md` 固化了历史上真正复现的 13 个标签家族，复用优先、新标签需一行理由——让跨报告趋势聚合从设计变成可实现。
- **评分锚定**：六维 1-10 附行为锚点；"维持既有习惯封顶 9 分"；某维度存在关联问题标签时不得打 10；评分理由必须引用具体行为。
- **模板 16 章 → 8 章 + TL;DR**：合并重复章节（评分卡与趋势、两个词典、改进/标签/提示词三章合一），产品判断改为条件章节，同一教训只写一次。
- **长度预算**：阶段复盘硬上限 15k 字符，超出必须删减。
- 旧报告（schema v1）无需迁移：`find_previous.sh` 按 `source_repo` 兼容读取旧 frontmatter；validator 只约束新报告。

## 适合谁

- 主要通过 Codex、Claude Code、OpenCode、Cursor、Trae 等 AI 编程工具做项目
- 不是传统程序员，但希望理解项目是怎么被做出来的
- 想复盘自己如何给 AI 下任务、控范围、验收结果
- 想在多次项目之间追踪自己的重复问题和进步趋势

## 快速安装

Codex 示例：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/PerpperQAQ/vibe-coding-review.git ~/.codex/skills/vibe-coding-review
```

Claude Code、OpenCode 或其他支持本地 skills 的工具：把整个仓库放到该工具约定的 skills 目录，保留 `SKILL.md`、`references/`、`scripts/` 的相对结构，然后重新加载 skills。

## 首次使用：固定输出目录（强烈建议）

skill 会按顺序解析输出目录（用户指定 > skill 安装目录 `.local/output-location.md` > 项目内 `.vibe-coding-review/output-location.md` > 环境变量 `VIBE_CODING_REVIEW_DIR` > 自动发现云盘/笔记目录）。**自动发现只作为一次性引导**：v2 规定首次通过自动发现解析成功后，必须把结果写进 `.local/output-location.md` 并告知你——避免每个新会话重新"掷骰子"（历史数据中逐会话自动发现的失败率高达 46%，个人复盘曾泄漏进项目仓库）。

手动配置示例（`~/.codex/skills/vibe-coding-review/.local/output-location.md`，已被 .gitignore 排除）：

```markdown
review_root: /Users/me/Documents/Obsidian/Vibe coding复盘
```

所有兜底路径都不会把个人复盘写进项目仓库；无法解析时 skill 会停下来问你。

## 最小使用

```text
使用 $vibe-coding-review 给这个项目做一次个人阶段复盘。
范围：最近 3 次 commit 和当前窗口完整上下文。
```

完整项目复盘、月度汇总同理，说明类型即可。多窗口证据是显式提供制：把导出记录的文件路径写进请求，skill 只读你提供的文件，不会自行扫描历史 sessions。

## 它会生成什么

中文 Markdown 报告，适合 Obsidian。阶段复盘固定结构：

- **TL;DR**（3 行：最重要教训 / 明天动作 / 下次提示词约束）
- 本阶段做了什么（含项目位置）
- 推进流程与 AI 指挥
- 架构理解
- 本阶段词典（≤6 条，含"你应该能复述成什么"）
- 产品判断（条件章节）
- Debug 与返工
- 评分卡与趋势（一张表，含上次分数与行为化理由）
- 问题、标签与下次约束（≤3 个问题，每个闭环到一条可复制的提示词片段；可选 1-3 条行动作业）
- 附录：证据盘点

## 评分维度

| 维度 | 关注点 |
|---|---|
| 项目推进清晰度 | 目标、范围、阶段边界、推进节奏是否清楚 |
| 架构理解程度 | 是否理解项目结构、模块职责和关键流程 |
| AI 指挥质量 | 提示词是否清楚，是否给出约束、验收标准和禁止事项 |
| 产品判断质量 | 是否理解用户价值、功能闭环、商业或使用场景 |
| 验收与测试意识 | 是否用测试、截图、日志、用户路径证明结果 |
| 复利沉淀质量 | 是否把经验转成下次可复用的知识、标签和约束 |

评分附行为锚点：10 分要求本阶段出现从未做到过的新负责人行为且有证据；维持既有习惯封顶 9 分；存在关联问题标签的维度不得满分。

## 仓库结构

```text
.
├── SKILL.md                       # 触发边界、工作流、评分与标签规则、校验步骤
├── references/
│   ├── report-templates.md        # 阶段/完整/月度三套模板（schema_version 2）
│   ├── tag-vocabulary.md          # 受控标签词表与评分封顶映射
│   └── examples.md                # 触发、查找、新标签、多窗口、月度的执行样例
├── scripts/
│   ├── find_previous.sh           # 按 source_repo 查找历史报告 / 聚合标签频次
│   └── validate_report.py         # 交付前校验（frontmatter/文件名/章节/表格/长度）
└── agents/
    └── openai.yaml                # 可选展示元数据
```

## 隐私提醒

复盘报告可能包含本地路径、聊天记录、commit、部署地址、产品想法、错误日志。公开或分享报告前请自行检查。skill 要求 AI 不编造缺失证据、不把证据边界说成已验证、不在可复用提示词片段里内嵌本机绝对路径，但具体材料能否公开仍需你自己判断。

## 校验

```bash
python3 scripts/validate_report.py <某份报告.md>
bash scripts/find_previous.sh <复盘目录> <项目仓库绝对路径>
```

两个脚本均无第三方依赖。
