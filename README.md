# project-handoff（项目交接 · WorkBuddy 版）

把长任务在**跨对话**时的进度、决定与下一步整理成结构化快照，让下一段对话能直接接手继续，免去重复说明与两边同时改。

本仓库是 [`duoduoler-ops/Table-skills`](https://github.com/duoduoler-ops/Table-skills) 中 `project-handoff` 技能的 **WorkBuddy 适配版**。

## 与原 Codex 版的区别

| 原 Codex 版 | 本 WorkBuddy 版 |
| --- | --- |
| `create_thread` / `list_projects` / `send_message_to_thread` 跨对话 thread API | 无——新对话说「继续 \<项目\>」，WorkBuddy 记忆自动注入索引并读取 `PROJECT_STATE.md` |
| `PostCompact` / `Stop` Hook + `compaction_reminder.py` 压缩计数 | 无——交接提醒由 agent 在阶段切换 / 可独立验收时自主评估（纯 prompt 逻辑） |
| `scripts/`、`hooks/`、`compaction-reminder.md` | 已移除，零外部脚本、零 Host Hook 依赖 |

核心思路不变：保存「目标 / 有效决定 / 关键文件 / 真实进度 / 下一步」，让接手方能先核对再继续。

## 安装

将整个 `project-handoff/` 目录放到 WorkBuddy 的技能目录：

- 用户级（推荐，跨项目可用）：`~/.workbuddy/skills/project-handoff/`
- 项目级：`{工作区}/.workbuddy/skills/project-handoff/`

> 保留整个目录，只复制 `SKILL.md` 无法替代配套的 `references/` 说明。

## 使用

- **保存进度**：说「保存进度 / 交接一下 / 整理项目状态」→ 双写：
  - 详细材料写入项目根 `PROJECT_STATE.md`；
  - 在工作区 `.workbuddy/memory/MEMORY.md` 追加一行索引，新对话自动可见。
- **接手继续**：开新对话说「继续 \<项目名\>」，WorkBuddy 从记忆读到索引 → 读 `PROJECT_STATE.md` → 先核对再推进。
- **恢复查看**：说「接着做 / 换对话继续」，先定位并只读核对交接材料，不会擅自覆盖新决定。

## 目录结构

```
project-handoff/
├── SKILL.md            # 入口 / 评估 / 展示 / 记忆整合
└── references/
    └── handoff.md      # 保存、恢复与手动接续
```

## 许可

基于 [`duoduoler-ops/Table-skills`](https://github.com/duoduoler-ops/Table-skills) 改造，沿用 [MIT License](LICENSE)。
