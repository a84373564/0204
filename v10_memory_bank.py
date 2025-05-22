#!/usr/bin/env python3
# v10_memory_bank.py - 模組失敗記憶儲存器（保留最多 300 筆）

import os, json
from datetime import datetime

MODULE_DIR = "/mnt/data/killcore/modules"
MEMORY_PATH = "/mnt/data/killcore/memory_bank.json"
MAX_MEMORY = 300

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def extract_memory(mod):
    return {
        "name": mod.get("name"),
        "symbol": mod.get("symbol"),
        "strategy": mod.get("strategy"),
        "score": mod.get("score"),
        "metrics": mod.get("metrics"),
        "died_at": datetime.utcnow().isoformat() + "Z"
    }

def main():
    memory = load_json(MEMORY_PATH)
    memory = memory[:MAX_MEMORY]  # 防呆保險

    survivors = []
    all_files = [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]

    for fname in all_files:
        path = os.path.join(MODULE_DIR, fname)
        with open(path, "r") as f:
            mod = json.load(f)
        survivors.append(mod.get("name"))

    # 查找死去的模組記憶（不在 survivors 裡）
    all_known = {m["name"]: m for m in memory}
    updated_memory = []

    for mname in all_known:
        if mname in survivors:
            updated_memory.append(all_known[mname])

    # 加入這一輪被淘汰的模組
    deleted_dir = "/mnt/data/killcore/deleted"
    os.makedirs(deleted_dir, exist_ok=True)
    deleted_files = [f for f in os.listdir(deleted_dir) if f.endswith(".json")]

    for fname in deleted_files:
        path = os.path.join(deleted_dir, fname)
        with open(path, "r") as f:
            mod = json.load(f)
        updated_memory.insert(0, extract_memory(mod))  # 新的放前面

    # 裁切只保留最新 300 筆
    updated_memory = updated_memory[:MAX_MEMORY]
    save_json(MEMORY_PATH, updated_memory)

    print(f"[v10] 已更新記憶庫，共記錄死亡模組：{len(updated_memory)} 筆")

if __name__ == "__main__":
    main()
