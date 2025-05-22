#!/usr/bin/env python3
# v09_core_engine.py - 王者唯一決選模組（Killcore 核心淘汰引擎）

import os, json, shutil

MODULE_DIR = "/mnt/data/killcore/modules"
KING_PATH = "/mnt/data/killcore/king_pool.json"
RANKING_PATH = "/mnt/data/killcore/module_ranking.json"
ARCHIVE_DIR = "/mnt/data/killcore/archives"

MAX_MODULES = 500          # 每輪最多模組數（控制刪除）
ARCHIVE_LIMIT = 50         # 最多保留幾隻歷代王者

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

    king = ranking[0]
    save_json(KING_PATH, king)
    archive_king(king)

    # 移除非王者模組
    for fname in os.listdir(MODULE_DIR):
        if fname.endswith(".json") and fname != king["name"]:
            os.remove(os.path.join(MODULE_DIR, fname))

    print(f"[v09] 王者誕生：{king['name']}")
    print(f"[v09] 已封存至：{KING_PATH}")
    print(f"[v09] 所有非王者模組已淘汰，保留 1 隻")

if __name__ == "__main__":
    main()
