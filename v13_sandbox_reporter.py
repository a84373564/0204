#!/usr/bin/env python3
# v13_sandbox_reporter.py - 王者報表生成器（現任＋歷代）

import json
import os

KING_PATH = "/mnt/data/killcore/king_pool.json"
ARCHIVE_PATH = "/mnt/data/killcore/v14_king_archive.json"
OUTPUT_PATH = "/mnt/data/killcore/king_summary.txt"

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def display_report(data):
    lines = []
    lines.append("[ 王者資訊報表 v13.1 - summary only ]")
    lines.append("")
    lines.append(f"模組名稱: {data.get('name', 'N/A')}")
    lines.append(f"幣別: {data.get('symbol', 'N/A')}")
    lines.append(f"策略類型: {data.get('type', 'N/A')}")
    lines.append(f"總分: {data.get('score', 'N/A')}")
    lines.append("")
    lines.append("平均績效:")
    lines.append(f"  - 平均獲利: {data.get('avg_profit', 'None')}")
    lines.append(f"  - 平均回撤: {data.get('avg_drawdown', 'None')}")
    lines.append(f"  - 平均勝率: {data.get('avg_win_rate', 'None')}")
    lines.append(f"  - 平均 Sharpe: {data.get('avg_sharpe', 'None')}")
    lines.append("")
    lines.append("資金配置:")
    lines.append(f"  - 配置資金: {data.get('capital', 'N/A')} USDT")
    lines.append(f"  - 可用總資金: {data.get('available', 'N/A')} USDT")
    lines.append(f"  - 來源: {data.get('source', 'N/A')}")
    lines.append("")
    lines.append("實戰沙盤:")
    lines.append(f"  - Profit: {data.get('real_profit', 'N/A')}")
    lines.append(f"  - Drawdown: {data.get('real_drawdown', 'N/A')}")
    lines.append(f"  - Sharpe: {data.get('real_sharpe', 'N/A')}")
    lines.append(f"  - Win rate: {data.get('real_win_rate', 'N/A')}")
    lines.append("")
    lines.append("=== 結束 ===")
    return "\n".join(lines)

def display_archive_top5():
    archive = load_json(ARCHIVE_PATH)
    if not archive:
        return "歷代王者紀錄：查無資料"

    sorted_mods = sorted(archive, key=lambda x: x.get("score", 0), reverse=True)
    top5 = sorted_mods[:5]

    lines = ["歷代前五名紀錄:"]
    for mod in top5:
        name = mod.get("name", "未知")
        symbol = mod.get("symbol", "N/A")
        score = mod.get("score", "N/A")
        lines.append(f"- {name} / {symbol} / score={score}")
    return "\n".join(lines)

def main():
    king = load_json(KING_PATH)
    report = display_report(king)
    history = display_archive_top5()

    with open(OUTPUT_PATH, "w") as f:
        f.write(report + "\n\n" + history + "\n")

    print(report)
    print()
    print(history)

if __name__ == "__main__":
    main()
