#!/usr/bin/env python3
# v09_core_engine.py - 王者唯一決選模組（Killcore 核心淘汰引擎）

import os, json, shutil

MODULE_DIR = "/mnt/data/killcore/modules"
KING_PATH = "/mnt/data/killcore/king_pool.json"
RANKING_PATH = "/mnt/data/killcore/module_ranking.json"
ARCHIVE_DIR = "/mnt/data/killcore/archives"

MAX_MODULES = 500
ARCHIVE_LIMIT = 50

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def archive_king(new_king):
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    all_archives = sorted(
        [f for f in os.listdir(ARCHIVE_DIR) if f.endswith(".json")],
        key=lambda x: os.path.getctime(os.path.join(ARCHIVE_DIR, x))
    )
    if len(all_archives) >= ARCHIVE_LIMIT:
        os.remove(os.path.join(ARCHIVE_DIR, all_archives[0]))
    archive_path = os.path.join(ARCHIVE_DIR, f"{new_king['name']}.json")
    save_json(archive_path, new_king)

def main():
    ranking = load_json(RANKING_PATH)
    if not ranking or not isinstance(ranking, list):
        print("[v09] 找不到有效排名資料")
        return

    new_king = ranking[0]
    old_king = load_json(KING_PATH)

    # 檢查是否連任，保留 king_count
    if old_king and old_king.get("name") == new_king.get("name"):
        new_king["king_count"] = old_king.get("king_count", 1) + 1
    else:
        new_king["king_count"] = 1

    save_json(KING_PATH, new_king)
    archive_king(new_king)

    # 刪除非王者模組
    for fname in os.listdir(MODULE_DIR):
        if fname.endswith(".json") and fname != new_king["name"] + ".json":
            os.remove(os.path.join(MODULE_DIR, fname))

    print(f"[v09] 王者誕生：{new_king['name']}（第 {new_king['king_count']} 次）")
    print(f"[v09] 已封存至：{KING_PATH}")
    print(f"[v09] 非王者模組已清除完畢，保留 1 隻")

if __name__ == "__main__":
    main()
