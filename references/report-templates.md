# Report Templates (schema_version 2)

Use these templates as the stable shape of the report. Keep every required section; adapt subsection depth to the evidence. Length budgets are hard limits enforced by `scripts/validate_report.py` — when over budget, cut lower-value detail instead of appending.

Writing red lines (apply to every template):

- Every score reason must cite one concrete behavior or quote from this stage.
- Every dictionary entry keeps the "你应该能复述成什么" column, written in first person where possible.
- Every problem in §8 keeps the four parts: 问题 / 证据 / 影响 / 下次怎么改.
- English engineering terms get a short Chinese gloss on first use, or an entry in §4; at most 10 unglossed terms per report.
- No absolute local paths inside reusable prompt fragments.

## 阶段复盘模板（content budget: soft 12k / hard 15k chars）

````markdown
---
type: vibe-coding-review
schema_version: 2
project: 项目名
review_type: 阶段复盘
created: YYYY-MM-DD HH:mm
source_repo: /absolute/path/to/repo
scope: 本次复盘范围
baseline_commit: commit-or-null
head_commit: commit-or-null
tags:
  - vibe-coding
  - project-review
  - learning-compound
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
---

# YYYY-MM-DD HH:mm｜项目名｜阶段N 主题 阶段复盘

## TL;DR

- 本阶段最重要的一个教训：
- 明天要做的一个动作：
- 下次提示词必加的一条约束：

## 1. 本阶段做了什么

先用一句话说明本阶段在项目中的位置（打地基/补功能/修体验/修质量/部署上线/调整方向），再用项目负责人能复述的语言总结成果，不罗列文件。

### 交付结果

-

### 尚未闭合的事项

-

## 2. 推进流程与 AI 指挥

| 步骤 | 发生了什么 | 你的角色 | AI 的角色 | 评价 |
|---|---|---|---|---|
| 1 |  |  |  |  |

### 指挥质量判断

- 有效的地方：
- 模糊或缺失验收标准的地方：
- 下次应提前定义的东西：

## 3. 架构理解

| 模块/文件 | 它负责什么 | 本阶段变化 | 你需要理解到什么程度 |
|---|---|---|---|
|  |  |  |  |

用一句话解释架构变化：

从用户动作到系统响应的流程（3-7 步）：

## 4. 本阶段词典

选本阶段最值得掌握的概念，至多 6 条（含需要解释的代码概念）。结合当前项目解释，不写通用百科定义。

| 概念 | 在本项目里是什么意思 | 为什么本阶段需要它 | 你应该能复述成什么 |
|---|---|---|---|
|  |  |  |  |

## 5. 产品判断

条件章节：仅当本阶段发生了真实的产品决策、方向变化或用户价值验证时展开（当前更完整的地方 / 仍缺的闭环 / 下一步验证）。否则只写一行：

本阶段无新增产品判断，沿用上次结论（上次报告文件名）。

## 6. Debug 与返工

| 问题 | 表现 | 解决方式 | 可复用经验 |
|---|---|---|---|
|  |  |  |  |

没有明确 debug 证据时，写明未发现相关记录。

## 7. 评分卡与趋势

评分前必须运行 `scripts/find_previous.sh <review_dir> <source_repo>` 并把"上次"列填为其输出的上一份分数；声称"暂无可比较报告"必须引用脚本的零匹配输出。评分锚点与封顶规则见 SKILL.md Scoring。

| 维度 | 上次 | 本次 | 趋势 | 评分理由（必须引用本阶段具体行为或原话） | 改进方向 |
|---|---:|---:|---|---|---|
| 项目推进清晰度 |  | /10 | 上升/持平/下降/无法比较 |  |  |
| 架构理解程度 |  | /10 |  |  |  |
| AI 指挥质量 |  | /10 |  |  |  |
| 产品判断质量 |  | /10 |  |  |  |
| 验收与测试意识 |  | /10 |  |  |  |
| 复利沉淀质量 |  | /10 |  |  |  |

趋势解释写行为变化，不复述数字。

## 8. 问题、标签与下次约束

本阶段最重要的问题，至多 3 个。每个问题一个小节，闭环写完不在别处重复：

### 8.1 问题标题

- 问题：
- 证据：
- 影响：
- 标签：（复用优先，见 references/tag-vocabulary.md；新标签须附一行"新标签理由：……"）
- 上次状态：（该标签上次出现时的阻断动作是否被执行；首次出现写"首次"）
- 阻断动作：（下次的一条具体提示词或流程约束）
- 下次提示词片段：

```text
（可直接复制进未来提示词的一句约束，对应上面的阻断动作）
```

### 行动作业（可选，1-3 条）

偏项目理解的小作业，如复述链路、写验收句、画模块图。

1.

## 附录：证据盘点

| 证据类型 | 是否找到 | 关键内容 | 局限 |
|---|---:|---|---|
| 当前窗口完整上下文 | 是/否/受限 |  |  |
| 用户提供的导出记录/多窗口材料 | 是/否/受限 |  |  |
| 代码仓库与 Git 记录 | 是/否 |  |  |
| AI 计划/TODO/项目文档 | 是/否 |  |  |
| 报错/日志 | 是/否 |  |  |
| 测试/验收结果 | 是/否 |  |  |
| 截图/部署/PR | 是/否 |  |  |
| 上一份同项目复盘 | 是/否 |  |  |

- 范围：
- 基线：
- 证据边界：
````

## 完整复盘模板（content budget: soft 24k / hard 30k chars）

````markdown
---
type: vibe-coding-review
schema_version: 2
project: 项目名
review_type: 完整复盘
created: YYYY-MM-DD HH:mm
source_repo: /absolute/path/to/repo
scope: 完整项目
baseline_commit: commit-or-null
head_commit: commit-or-null
tags:
  - vibe-coding
  - project-review
  - learning-compound
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
---

# YYYY-MM-DD HH:mm｜项目名｜完整复盘

## TL;DR

- 这个项目最重要的一个教训：
- 下个项目第一天要做的一个动作：
- 下个项目提示词必加的一条约束：

## 1. 项目一句话总结与发展路径

一句话：这个项目为谁解决什么问题，现在做到什么状态。

| 阶段 | 目标 | 关键动作 | 结果 | 评价 |
|---|---|---|---|---|
| 1 |  |  |  |  |

## 2. 需求如何被拆成开发任务

拆分得好的地方 / 拆分得不好的地方。

## 3. 整体架构

用新手能懂的方式解释前端、后端、数据、第三方服务、部署之间的关系。

| 模块/目录 | 职责 | 为什么存在 | 你需要掌握的理解 |
|---|---|---|---|
|  |  |  |  |

最核心的一条数据流或用户流程（5-10 步）：

## 4. 项目词典

理解完整项目必须掌握的概念，5-8 条。

| 概念 | 在本项目里是什么意思 | 为什么它是核心 | 你应该能复述成什么 |
|---|---|---|---|
|  |  |  |  |

## 5. 核心功能与关键技术决策

| 功能/决策 | 用户价值或选择 | 实现概览/可能原因（推断需标注） | 完成度/替代方案 | 风险/复盘判断 |
|---|---|---|---|---|
|  |  |  |  |  |

## 6. AI 协作模式复盘

你主要把 AI 当成了什么；有效协作模式；低效协作模式；下个项目应该怎样指挥 AI。

## 7. 评分卡与趋势

同阶段模板：先运行 `scripts/find_previous.sh`，"上次"列引用最近一份同项目报告；锚点与封顶规则见 SKILL.md。

| 维度 | 上次 | 本次 | 趋势 | 评分理由（必须引用具体行为或原话） | 改进方向 |
|---|---:|---:|---|---|---|
| 项目推进清晰度 |  | /10 |  |  |  |
| 架构理解程度 |  | /10 |  |  |  |
| AI 指挥质量 |  | /10 |  |  |  |
| 产品判断质量 |  | /10 |  |  |  |
| 验收与测试意识 |  | /10 |  |  |  |
| 复利沉淀质量 |  | /10 |  |  |  |

## 8. 问题、标签与下次约束

项目中反复暴露的问题，至多 5 个，结构同阶段模板 §8（问题/证据/影响/标签/上次状态/阻断动作/下次提示词片段）。重点回答"这些问题为什么持续出现"，不要只写"下次注意"。

### 产品/商业落地判断

完整复盘必写：用户对象、使用场景、价值假设、交付形态、商业化或分发路径、下一步 go/no-go。证据不足时明确写"证据不足，只能做有限判断"。

### 这次项目真正积累下来的能力

只写证据能支持的能力，不写空泛鼓励。

### 行动作业（可选，1-3 条）

1.

## 附录：证据盘点

同阶段模板的证据表，另加：README/docs、issue/PR、部署证据。

- 范围：
- 证据边界：
````

## 月度复盘汇总模板（content budget: soft 16k / hard 20k chars）

````markdown
---
type: vibe-coding-review
schema_version: 2
project: 项目名或多项目
review_type: 月度复盘汇总
created: YYYY-MM-DD HH:mm
source_repo: null
scope: YYYY-MM 月度复盘汇总
included_reports:
  - report-file-name.md
aggregated_issue_tags:
  - tag-or-none
tags:
  - vibe-coding
  - project-review
  - learning-compound
  - monthly-review
---

# YYYY-MM｜项目名或多项目｜月度复盘汇总

## 0. 汇总范围

| 报告文件 | 项目 | 类型 | 日期 | 是否有评分 |
|---|---|---|---|---:|
|  |  |  |  | 是/否 |

- 月份 / 纳入报告数量 / 排除或缺失的报告 / 证据边界：

## 1. 本月总体判断

项目负责人视角：推进是否更清楚、架构理解是否变强、AI 指挥是否更有效、产品判断是否更成熟。

## 2. 评分变化趋势

| 维度 | 期初 | 期末 | 趋势 | 变化解释（写行为变化，不只算平均分） |
|---|---:|---:|---|---|
| 项目推进清晰度 |  |  |  |  |
| 架构理解程度 |  |  |  |  |
| AI 指挥质量 |  |  |  |  |
| 产品判断质量 |  |  |  |  |
| 验收与测试意识 |  |  |  |  |
| 复利沉淀质量 |  |  |  |  |

## 3. 重复问题标签趋势与成因

用 `scripts/find_previous.sh <dir> <repo> --tags` 的频次输出作为本表依据。对最重要的 1-3 个标签做成因分析；成因必须从报告证据推出，不写人格判断。

| 标签 | 出现次数/报告 | 上月阻断动作是否生效 | 成因判断 | 下月阻断动作 |
|---|---|---|---|---|
|  |  |  |  |  |

## 4. 能力与产品判断变化

证据能支持的能力变化；产品/商业判断是否更清晰；下月最该验证的问题。

## 5. 本月保留与改变

- 最值得保留的做法：
- 下月真正需要改变的 1-3 个负责人行为（对应本月报告证据）：

## 6. 下月提示词优化方向

把本月重复出现的问题转化为下月固定加入的提示词约束，2-4 条，每条对应一个标签：

```text
-
```
````
