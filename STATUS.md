# STATUS (update before every meeting) — 最后更新: 2026-10-24

分三档,和 Project Plan §4 的口径一致。**没有证据的不要往上档写。**

## 已实现 (Implemented: 代码在仓库、能跑、有测试)
- 曝光指标:stance 分布(排除 unknown)、熵、JSD、reason coverage、来源重复度、滑动窗口 — `src/fbx/exposure.py`
- 标注质量:一致率、Cohen's kappa、分歧列表 — `src/fbx/annotation.py`
- 玩具仿真:规则型推荐器 + 规则型用户 + 5 种干预策略 + 匹配种子比较 + 敏感性(标签错误率、用户倾向)
- 单元测试 5 个(指标边界、unknown/稀疏处理、kappa、仿真可复现、空 feed 不算成功)

## 已验证 (Validated: 用真实数据/真人核对过)
- (空) — 目前没有任何组件在真实标注或真实数据上验证过。
  验证后在这里写:数据来源、样本量、数字。

## 仅提出 / 待做 (Proposed)
- [ ] 选定两个议题 + 一个留出议题;定义 claim 与参考理由语料(附来源)
- [ ] 真实 pilot 标注(Fu / Wang 独立标注)→ 跑 `run_annotation_agreement.py`
- [ ] 用 ShortVideo 的 8 组视频-转写对做第一份真实 worked example
- [ ] LLM/VLM 抽取 + 仅标题/转写/视觉三种输入对比(precision/recall)
- [ ] 在 KuaiRand/ShortVideo 留出日志上做用户模型校准;换用户模型看最优策略是否反转
- [ ] 留出议题评估;更完整的敏感性分析

## 已知限制
- 仿真参数(提升倍数、遗忘率、预算)是人为设定,结果只在该设定内成立
- demo 数据是合成的,不能写进报告当结果
- 标签噪声目前是随机翻转,真实 LLM 错误更有结构(如把角色台词归给创作者)
