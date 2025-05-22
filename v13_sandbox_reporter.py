#!/usr/bin/env python3
# v13_sandbox_reporter.py - 王者報表顯示器（summary only）

import json
import os

KING_PATH = "/mnt/data/killcore/king_pool.json"
HISTORY_PATH = "/mnt/data/killcore/king_archive.json"
SUMMARY_PATH = "/mnt/data/killcore/king_summary.txt"

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def write_summary(lines):
    with open(SUMMARY_PATH, "w") as f:
        f.write("\n".join(lines))

def summarize():
    king = load_json(KING_PATH)
    history_data = load_json(HISTORY_PATH)

    # 兼容格式：list（舊格式）或 dict（新格式含 "history"）
    if isinstance(history_data, list):
        history = history_data
    elif isinstance(history_data, dict):
        history = history_data.get("history", [])
    else:
        history = []

    lines = []
    lines.append("[ 王者資訊報表 v13.2 - summary only ]\n")

    if not king:
        lines.append("目前尚無王者")
        write_summary(lines)
        return

    lines.append(f"模組名稱: {king.get('name')}")
    lines.append(f"幣別: {king.get('symbol')}")
    lines.append(f"策略類型: {king.get('type')}")
    lines.append(f"總分: {round(king.get('score', 0), 4)}\n")

    lines.append("平均績效:")
    lines.append(f" - 平均獲利: {king.get('avg_profit', 'None')}")
    lines.append(f" - 平均回撤: {king.get('avg_drawdown', 'None')}")
    lines.append(f" - 平均勝率: {king.get('avg_win_rate', 'None')}")
    lines.append(f" - 平均 Sharpe: {king.get('avg_sharpe', 'None')}\n")

    lines.append("資金配置:")
    lines.append(f" - 配置資金: {king.get('capital', 'N/A')} USDT")
    lines.append(f" - 可用總資金: {king.get('capital_total', 'N/A')} USDT")
    lines.append(f" - 來源: {king.get('capital_source', 'N/A')}\n")

    lines.append("實戰沙盤:")
    lines.append(f" - Profit: {king.get('real_profit', 'N/A')}")
    lines.append(f" - Drawdown: {king.get('real_drawdown', 'N/A')}")
    lines.append(f" - Sharpe: {king.get('real_sharpe', 'N/A')}")
    lines.append(f" - Win rate: {king.get('real_win_rate', 'N/A')}\n")

    lines.append("血統資訊:")
    lines.append(f" - 是否為重生者: {king.get('from_retry', False)}")
    lines.append(f" - 衛冕次數: {king.get('defend_count', 0)}")
    if king.get("defend_count", 0) == 0:
        lines.append(" - 備註: 首次登基\n")
    else:
        lines.append("")

    lines.append("歷代前五名紀錄:")
    if not history:
        lines.append(" - 查無資料")
    else:
        top = sorted(history, key=lambda x: x.get("score", 0), reverse=True)[:5]
        for item in top:
            lines.append(f"- {item.get('name')} / {item.get('symbol')} / score={round(item.get('score', 0), 4)}")

    lines.append("\n=== 結束 ===")
    write_summary(lines)
    for line in lines:
        print(line)

if __name__ == "__main__":
    summarize()
