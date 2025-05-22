#!/usr/bin/env python3
# v15_memory_heatmap_tracker.py - 統計死亡記憶熱點與失敗常見指標

import json
import os
from collections import defaultdict

MEMORY_PATH = "/mnt/data/killcore/memory_bank.json"
HEATMAP_PATH = "/mnt/data/killcore/memory_heatmap.json"

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []

def main():
    memory = load_json(MEMORY_PATH)
    if not memory:
        print("[v15] 無法載入記憶庫")
        return

    heatmap = defaultdict(list)

    for entry in memory:
        metrics = entry.get("metrics", {})
        for key, val in metrics.items():
            heatmap[key].append(val)

    result = {}
    for key, values in heatmap.items():
        avg = round(sum(values) / len(values), 4)
        worst = round(min(values), 4)
        best = round(max(values), 4)
        result[key] = {
            "count": len(values),
            "average": avg,
            "worst": worst,
            "best": best
        }

    with open(HEATMAP_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[v15] 死亡熱點報表已生成：{HEATMAP_PATH}")

if __name__ == "__main__":
    main()
