#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
precompact_reminder.py — WorkBuddy PreCompact Hook (project-handoff skill)

在 WorkBuddy 即将压缩会话上下文之前触发。
目的：
  1) 向「用户」弹出系统提示，建议先保存交接进度（project-handoff skill）；
  2) 向「Agent」注入压缩指导，确保压缩后仍保留项目目标、关键决策、
     文件路径与下一步，便于新对话接手。

输入：stdin 上的 JSON（PreCompact 事件载荷）
输出：stdout 上的 JSON
  - systemMessage                        -> 展示给终端用户（用户可见）
  - hookSpecificOutput.additionalContext -> 注入给 Agent 作为压缩指导（跨压缩保留）
退出码 0 = continue（不阻断压缩本身）。

仅「提醒」，不自动保存——遵守 skill 原则「提醒不会自动执行交接」。
"""

import sys
import json


def main():
    # 强制 UTF-8 输出，保证中文提醒正确渲染。
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    # 读取事件载荷（防御：stdin 可能为空或非 JSON）。
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        payload = {}

    trigger = payload.get("trigger", "auto")  # "auto" | "manual"
    # cwd = payload.get("cwd", "")  # 预留：将来可按项目决定是否提醒

    # --- 展示给「用户」的系统消息（用户可见） ---
    user_msg = (
        "⚠️ 上下文即将压缩（%s）。若当前任务有跨对话价值，"
        "建议先说「保存进度 / 交接一下」——我会把目标、关键决策、"
        "文件路径与下一步写入 PROJECT_STATE.md，下次新对话说"
        "「继续 <项目名>」即可无缝接手。" % trigger
    )

    # --- 注入给「Agent」的压缩指导（压缩后仍保留） ---
    agent_ctx = (
        "即将进行上下文压缩。若当前任务有跨对话价值，请在压缩摘要中优先保留："
        "项目目标、已确认的关键决策、关键文件路径、当前真实进度与下一步。"
        "若尚未生成 PROJECT_STATE.md，压缩后第一件事应先提醒用户保存交接进度"
        "（说「保存进度」即可），不要擅自覆盖任何已有决定。"
    )

    out = {
        "continue": True,
        "systemMessage": user_msg,
        "hookSpecificOutput": {
            "hookEventName": "PreCompact",
            "additionalContext": agent_ctx,
        },
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False))
    sys.stdout.write("\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
