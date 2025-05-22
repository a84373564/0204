#!/usr/bin/env python3
# v14_king_archive.py - 整合歷代王者封存資料為統一報表（由 king_archive.json 匯出）

import json
import os

ARCHIVE_PATH = "/mnt/data/killcore/king_archive.json"
REPORT_PATH = "/mnt/data/killcore/king_history_report.json"

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []

def generate_summary(archive):
    summary = []
    for king in archive:
        summary.append({
            "name": king.get("name"),
            "symbol": king.get("symbol"),
            "score": king.get("score"),
            "strategy": king.get("strategy"),
            "archived_at": king.get("archived_at", "N/A"),
            "avg_profit": king.get("metrics", {}).get("avg_profit"),
            "avg_drawdown": king.get("metrics", {}).get("avg_drawdown"),
            "avg_win_rate": king.get("metrics", {}).get("avg_win_rate"),
            "avg_sharpe": king.get("metrics", {}).get("avg_sharpe")
        })
    return summary

def main():
    archive = load_json(ARCHIVE_PATH)
    if not archive:
        print("[v14] 找不到王者封存資料")
        return

    summary = generate_summary(archive)
    with open(REPORT_PATH, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"[v14] 歷代王者報表已匯出：{REPORT_PATH}（共 {len(summary)} 筆）")

if __name__ == "__main__":
    main()
