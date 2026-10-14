#!/usr/bin/env python3
"""探测本机当前可用的合规检测通道，决定本次审查走哪条路径。

设计原则：
- 只报告凭据「是否存在」，**永不打印凭据的值**（连前后几位都不打）。
- 探测不联网、不花钱、不写文件；它只回答「现在能用什么」。
- 没有任何凭据是正常状态，不是错误：此时走零接入路径，退出码仍为 0。

用法：
    python3 scripts/detect_capabilities.py           # 人读的表格
    python3 scripts/detect_capabilities.py --json    # 机读的 JSON

凭据只认环境变量：TroHub、LinkFox 的客户端都从环境变量取 key，写在文件里它们读不到。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# LinkFox 厂商 skill 仓（睿观各路走它的脚本）。装在别处时用 LINKFOX_SKILLS_DIR 指定。
LINKFOX_SKILL_DIRS = [
    Path(os.environ["LINKFOX_SKILLS_DIR"]) if os.environ.get("LINKFOX_SKILLS_DIR") else None,
    Path.home() / ".codex" / "skills",
    Path.home() / ".claude" / "skills",
    Path.home() / "skills",
]

TROHUB_SKILL_DIRS = [
    Path.home() / ".codex" / "skills" / "trohub-ip-check",
    Path.home() / ".claude" / "skills" / "trohub-ip-check",
]


def has_credential(*candidates: str) -> tuple[bool, str | None]:
    """凭据是否可得（只看环境变量）。返回 (是否存在, 来源)，不返回值本身。"""
    for name in candidates:
        if os.environ.get(name):
            return True, f"环境变量 {name}"
    return False, None


def first_existing(paths) -> Path | None:
    for p in paths:
        if p and p.exists():
            return p
    return None


def detect() -> dict:
    trohub_key, trohub_src = has_credential("TROHUB_API_KEY")
    trohub_dir = first_existing(TROHUB_SKILL_DIRS)
    linkfox_key, linkfox_src = has_credential("LINKFOX_AGENT_API_KEY", "LINKFOXAGENT_API_KEY")
    linkfox_dir = first_existing(LINKFOX_SKILL_DIRS)

    channels = [
        {
            "id": "trohub",
            "名称": "TroHub 图像三库 + 文字商标 + TRO 案例",
            "覆盖": ["外观专利", "图形商标", "版权形象", "文字商标", "TRO 情报"],
            "可用": bool(trohub_key and trohub_dir),
            "凭据": trohub_src,
            "入口": str(trohub_dir / "scripts" / "trohub_client.py") if trohub_dir else None,
            "单价": "三库全扫 35 积分/图 ≈ ¥1–1.4；文字商标 2 积分 ≈ ¥0.06",
            "限流": "图像 10 次/分，商标与专利反查 30 次/分，并发 ≤3",
            "缺什么": None if (trohub_key and trohub_dir)
                      else ("缺 TROHUB_API_KEY" if not trohub_key else "缺 trohub-ip-check skill 目录"),
        },
        {
            "id": "ruiguan",
            "名称": "睿观六路（经 LinkFox 网关）",
            "覆盖": ["实用新型/发明专利", "图片政策合规", "外观专利", "图形商标", "版权形象", "文字商标"],
            "可用": bool(linkfox_key and linkfox_dir),
            "凭据": linkfox_src,
            "入口": str(linkfox_dir) if linkfox_dir else None,
            "单价": "实用新型 ¥0.92；图片政策 ¥0.31；外观/图形商标 ¥0.61–0.92；版权 ¥0.31–0.61；文字商标 ¥0.31",
            "限流": "未公布；积分池与 LinkFox OS 任务共用",
            "缺什么": None if (linkfox_key and linkfox_dir)
                      else ("缺 LINKFOX_AGENT_API_KEY" if not linkfox_key
                            else "缺 LinkFox 厂商 skill 目录（设 LINKFOX_SKILLS_DIR 指定）"),
        },
        {
            "id": "zhihuiya",
            "名称": "智慧芽专利深核（直连 MCP）",
            "覆盖": ["专利法律状态", "权利要求", "同族", "是否失效"],
            "可用": None,  # MCP 由 harness 提供，脚本探测不到，运行时按工具是否存在判断
            "凭据": "由 MCP 提供",
            "入口": "mcp__zhihuiya-patent__*",
            "单价": "不耗 LinkFox 积分",
            "限流": "见各自套餐",
            "缺什么": "运行时检查会话里有没有 zhihuiya-patent 工具",
        },
        {
            "id": "sellersprite",
            "名称": "卖家精灵在册商标兜底（直连 MCP）",
            "覆盖": ["在册文字商标"],
            "可用": None,
            "凭据": "由 MCP 提供",
            "入口": "mcp__sellersprite-mcp__trademark_*",
            "单价": "走已购配额",
            "限流": "见各自套餐",
            "缺什么": "运行时检查会话里有没有 sellersprite-mcp 工具",
        },
    ]

    paid = [c for c in channels if c["可用"] is True]
    mode = "零接入" if not paid else "数据源增强"

    # 零接入路径下确定盖不住的风险面
    gaps = []
    if not any(c["可用"] for c in channels if c["id"] in ("trohub", "ruiguan")):
        gaps = ["外观专利（无图像比对）", "图形商标/logo（无图像比对）",
                "版权形象（仅靠模型识别知名 IP）", "实用新型/发明专利（仅靠公开库关键词）"]
    elif not any(c["可用"] for c in channels if c["id"] == "ruiguan"):
        gaps = ["实用新型/发明专利（TroHub 没有这一路）", "图片政策合规/禁售品视觉识别"]

    return {"模式": mode, "可用通道数": len(paid), "channels": channels, "零接入盖不住": gaps}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="输出 JSON 供程序消费")
    args = ap.parse_args()

    r = detect()
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    print(f"\n本次审查模式：{r['模式']}（付费通道可用 {r['可用通道数']} 条）\n")
    for c in r["channels"]:
        mark = {True: "可用", False: "不可用", None: "运行时判断"}[c["可用"]]
        print(f"  [{mark}] {c['名称']}")
        print(f"        覆盖：{'、'.join(c['覆盖'])}")
        if c["可用"] is True:
            print(f"        凭据：{c['凭据']}")
            print(f"        单价：{c['单价']}")
            print(f"        限流：{c['限流']}")
        elif c["缺什么"]:
            print(f"        缺口：{c['缺什么']}")
        print()

    if r["零接入盖不住"]:
        print("本次盖不住的风险面（报告必须声明）：")
        for g in r["零接入盖不住"]:
            print(f"  - {g}")
        print()
    print("提示：凭据只报告存在与否，本脚本不打印任何凭据的值。\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
