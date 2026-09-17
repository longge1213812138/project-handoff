# project-handoff（项目交接 · WorkBuddy 版）

把长任务在**跨对话**时的进度、决定与下一步整理成结构化快照，让下一段对话能直接接手继续，免去重复说明与两边同时改。

本仓库是 [`duoduoler-ops/Table-skills`](https://github.com/duoduoler-ops/Table-skills) 中 `project-handoff` 技能的 **WorkBuddy 适配版**。

## 与原 Codex 版的区别

| 原 Codex 版 | 本 WorkBuddy 版 |
| --- | --- |
| `create_thread` / `list_projects` / `send_message_to_thread` 跨对话 thread API | 无——新对话说「继续 \<项目\>」，WorkBuddy 记忆自动注入索引并读取 `PROJECT_STATE.md` |
| `PostCompact` / `Stop` Hook + `compaction_reminder.py` 压缩计数 | **有等价物**——`PreCompact` Hook（`hooks/precompact_reminder.py` + 在 `~/.codebuddy/settings.json` 注册），压缩前自动弹出系统提醒，并向 Agent 注入压缩指导 |
| `scripts/`、`compaction-reminder.md` | 已移除；改为 WorkBuddy 版 `hooks/`（仅一个标准库 Python 脚本，零第三方依赖） |

核心思路不变：保存「目标 / 有效决定 / 关键文件 / 真实进度 / 下一步」，让接手方能先核对再继续。

## 安装

将整个 `project-handoff/` 目录放到 WorkBuddy 的技能目录：

- 用户级（推荐，跨项目可用）：`~/.workbuddy/skills/project-handoff/`
- 项目级：`{工作区}/.workbuddy/skills/project-handoff/`

> 保留整个目录，只复制 `SKILL.md` 无法替代配套的 `references/` 与 `hooks/`。

### 启用 PreCompact 自动提醒（可选，推荐）

本仓库附带一个 `PreCompact` Hook，能在 WorkBuddy **即将压缩上下文前**自动提醒你「保存进度」。启用方式：

把以下内容写入 **`~/.codebuddy/settings.json`**（已附 `hooks/workbuddy-hooks.example.json` 可直接参考；**注意目录名是 `codebuddy` 不是 `workbuddy`**）：

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "C:/Users/你的用户名/.workbuddy/skills/project-handoff/hooks/precompact_reminder.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

要点：

- `matcher` 留空匹配 auto / manual 两种压缩触发。
- Windows 下 Hook 以 Git Bash 运行，命令请写 **`C:/Users/...` 盘符写法**（Git Bash 不会误转换）；脚本本身依赖 `python3` 或写死解释器绝对路径均可，推荐写死以避开 PATH 问题。
- Hook **只「提醒」、不自动保存**——遵守 skill「提醒不会自动执行交接」原则。
- 不启用此 Hook 也完全可用：手动说「保存进度 / 交接一下」即可，或依赖 agent 在阶段切换时的自主评估。

## 使用

- **保存进度**：说「保存进度 / 交接一下 / 整理项目状态」→ 双写：
  - 详细材料写入项目根 `PROJECT_STATE.md`；
  - 在工作区 `.workbuddy/memory/MEMORY.md` 追加一行索引，新对话自动可见。
- **接手继续**：开新对话说「继续 \<项目名\>」，WorkBuddy 从记忆读到索引 → 读 `PROJECT_STATE.md` → 先核对再推进。
- **恢复查看**：说「接着做 / 换对话继续」，先定位并只读核对交接材料，不会擅自覆盖新决定。
- **自动提醒**：若已启用 PreCompact Hook，上下文即将压缩时会自动弹系统提醒，提示先保存。

## 目录结构

```
project-handoff/
├── SKILL.md                                 # 入口 / 评估 / 展示 / 记忆整合
├── references/
│   └── handoff.md                           # 保存、恢复与手动接续
└── hooks/
    ├── precompact_reminder.py               # PreCompact 自动提醒脚本（仅标准库）
    └── workbuddy-hooks.example.json         # settings.json 注册示例
```

## 许可

基于 [`duoduoler-ops/Table-skills`](https://github.com/duoduoler-ops/Table-skills) 改造，沿用 [MIT License](LICENSE)。
