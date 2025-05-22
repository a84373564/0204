#!/usr/bin/env python3
# v11_king_pool.py - 保留唯一王者模組（含完整欄位）

import json
import os
from datetime import datetime

KING_PATH = "/mnt/data/killcore/king_pool.json"
POOL_PATH = "/mnt/data/killcore/king_archive.json"
MAX_KINGS = 50

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    king = load_json(KING_PATH)
    if not king or not isinstance(king, dict):
        print("[v11] 找不到有效王者資料")
        return

    archive = load_json(POOL_PATH)
    if not isinstance(archive, list):
        archive = []

    # 檢查是否已存在
    existing = [k for k in archive if k.get("name") == king.get("name")]
    if not existing:
        king["archived_at"] = datetime.utcnow().isoformat() + "Z"
        archive.insert(0, king)

    # 保留最多 50 筆
    archive = archive[:MAX_KINGS]
    save_json(POOL_PATH, archive)

    print(f"[v11] 王者資料已儲存至 king_archive.json，共 {len(archive)} 筆歷代王者")

if __name__ == "__main__":
    main()
