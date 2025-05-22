#!/usr/bin/env python3
# v13_sandbox_reporter.py - 顯示現任王者績效與指標報表

import json
import os

KING_PATH = "/mnt/data/killcore/king_pool.json"

def print_metrics(metrics):
    print("\n=== 王者績效指標 ===")
    for key, val in metrics.items():
        print(f"{key:25}: {val}")

def print_summary(mod):
    print("=== 王者模組資訊 ===")
    print(f"Name      : {mod.get('name')}")
    print(f"Symbol    : {mod.get('symbol')}")
    print(f"Strategy  : {mod.get('strategy')}")
    print(f"Score     : {mod.get('score')}")
    print(f"Created At: {mod.get('created_at', 'N/A')}")
    print_metrics(mod.get("metrics", {}))

def main():
    if not os.path.exists(KING_PATH):
        print("[v13] 無法找到 king_pool.json")
        return

    with open(KING_PATH, "r") as f:
        king = json.load(f)

    print_summary(king)

    with open("/mnt/data/killcore/king_report.json", "w") as f:
        json.dump(king, f, indent=2)

    print("\n[v13] 已匯出 king_report.json")

if __name__ == "__main__":
    main()
