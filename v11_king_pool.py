#!/usr/bin/env python3
# 強化版 v11_king_pool.py - 寫入王者模組時補齊沙盤績效與資金欄位

import os
import json
from datetime import datetime

KING_PATH = "/mnt/data/killcore/king_pool.json"
POOL_PATH = "/mnt/data/killcore/king_archive.json"
MODULE_DIR = "/mnt/data/killcore/modules"
MAX_KINGS = 50
PERFORMANCE_KEYS = ["profit", "drawdown", "sharpe", "win_rate"]

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {} if path.endswith(".json") else []

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def find_matching_module(mod_name):
    target_file = os.path.join(MODULE_DIR, mod_name)
    if os.path.exists(target_file):
        return load_json(target_file)
    return {}

def patch_performance(king):
    mod_data = find_matching_module(king.get("name", ""))
    for key in PERFORMANCE_KEYS:
        if key not in king or king[key] in [None, "N/A"]:
            if key in mod_data:
                king[key] = mod_data[key]
    if "capital" not in king and "capital" in mod_data:
        king["capital"] = mod_data["capital"]
    if "capital_source" not in king and "capital_source" in mod_data:
        king["capital_source"] = mod_data["capital_source"]
    return king

def main():
    king = load_json(KING_PATH)
    if not king or not isinstance(king, dict):
        print("[v11] 找不到有效王者資料")
        return

    king = patch_performance(king)

    archive = load_json(POOL_PATH)
    if not isinstance(archive, list):
        archive = []

    existing = [k for k in archive if k.get("name") == king.get("name")]
    if not existing:
        king["archived_at"] = datetime.utcnow().isoformat() + "Z"
        archive.insert(0, king)

    archive = archive[:MAX_KINGS]
    save_json(POOL_PATH, archive)
    print("[v11] 王者資料已補寫績效並封存成功")

if __name__ == "__main__":
    main()
