# Issue Tag Vocabulary（受控标签词表）

review_issue_tags 的唯一目的，是让同一个问题在多份报告之间可以被聚合和追踪。一次性标签做不到这件事。历史数据教训：188 个去重标签中 82% 只出现过一次，"没做真实验证"一个问题曾有 6 种写法，趋势分析因此失效。

## 使用规则

1. **复用优先**。写 review_issue_tags 前，先运行 `scripts/find_previous.sh <review_dir> <source_repo> --tags` 查看既有标签及频次；本次问题与某个既有标签描述的是同一行为时，必须复用该标签，不得起新名字。
2. **新标签需要一行理由**。核心词表和既有标签都不覆盖时才允许新建，且必须在报告 §8 对应问题下写一行"新标签理由：现有标签 X/Y 不覆盖，因为……"。
3. **禁止**：
   - 状态后缀入标签名（`-improved` / `-fixed` / `-resolved` / `-blocked`）。改善与否写在 §8 的"上次状态"或评分趋势解释里，标签名只描述问题本身。
   - 正向/表扬条目占用 review_issue_tags。进步属于评分趋势解释，不属于问题标签。
   - 阶段一次性任务描述当标签（如 `stage-6-25c-candidate-c-check`）。留在正文。
4. 全部小写 kebab-case。
5. prompt_constraint_tags 只收**可跨阶段复用**的约束模式（如 `user-path-validation-required`）；描述本阶段具体任务的约束写进正文 §8 的提示词片段，不进 frontmatter。

## 核心词表

历史 91 份报告中出现 ≥3 次的标签家族，已合并同义变体。括号内为该标签吸收的历史变体名，遇到同类行为一律用主标签。

| 标签 | 含义 | 典型证据 | 关联评分维度 |
|---|---|---|---|
| static-tests-over-real-validation | 用静态/自动化测试替代真实用户路径或真实客户端验证（吸收 real-user-path-validation-gap、real-client-validation-lag、real-validation-deferred、live-validation-deferred、missing-user-path-validation、missing-browser-manual-audible-validation） | 测试全绿但未跑真实客户端/真实数据/真实音画 | 验收与测试意识 |
| continue-next-stage-inertia | 未过验收门就说"继续下一阶段" | 阶段目标没有写成可判定的决策门就下达下一条指令 | 项目推进清晰度 |
| acceptance-overclaim-risk | 把部分完成表述成完成（吸收 mechanics-pass-not-quality-pass） | handoff/总结中的能力宣称超出证据等级 | 验收与测试意识 |
| vague-acceptance-criteria | 阶段开工时没有可判定的验收标准 | 提示词只有任务描述、没有"什么算完成" | AI 指挥质量 |
| stage-gate-discipline | 阶段边界/决策门纪律问题（吸收 stage-boundary-discipline、stage-boundary-protection） | 阶段切面混乱、dirty worktree 跨阶段、越权推进 | 项目推进清晰度 |
| overbroad-scope | 单阶段范围过大或被隐性扩展 | 一个阶段塞进多个不相关目标 | 项目推进清晰度 |
| multi-window-evidence-fragmentation | 阶段证据分散在多个窗口/会话且复盘时不可见 | 复盘只能从摘要重建过程 | 复利沉淀质量 |
| evidence-boundary-gap | 证据边界不清或证据缺失未被显式标注（吸收 evidence-directory-implicit、evidence-semantic-audit-required、evidence-binding-blind-spot、semantic-boundary-test-lag） | 结论与证据等级不匹配、证据目录隐式 | 验收与测试意识 |
| late-adversarial-matrix | 对抗性/失败面测试矩阵在实现后才补 | 独立审计追加发现 P1，初始任务卡没有威胁矩阵 | 验收与测试意识 |
| product-gate-gap | 产品闭环或产品验收门缺失（吸收 unclear-product-gate、product-loop-gap） | 功能完成但用户价值路径未定义/未验证 | 产品判断质量 |
| weak-architecture-recall | 无法复述模块职责或关键流程 | 复盘时说不清某文件归属或数据流 | 架构理解程度 |
| secret-handling-gap | 密钥/敏感信息处理不当（吸收 secret-in-chat-risk、secret-sharing-risk、secret-rotation-risk） | 真实 key 贴进聊天、明文越权可见 | AI 指挥质量 |
| mock-capability-boundary | mock/合成能力与真实能力边界混淆 | 把 synthetic 通过复述成真实能力 | 验收与测试意识 |

## 关联维度的用途（评分封顶规则）

评分卡中某维度打 10 分时，本报告 review_issue_tags 中不得存在"关联评分维度"为该维度的标签；存在则该维度上限 9。这条规则由上表机械可查，不依赖判断。
