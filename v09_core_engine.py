#!/usr/bin/env python3
# v09_core_engine.py - 王者唯一決選模組（修復版，支援連任與 king_count）

import os, json, shutil

MODULE_DIR = "/mnt/data/killcore/modules"
KING_PATH = "/mnt/data/killcore/king_pool.json"
RANKING_PATH = "/mnt/data/killcore/module_ranking.json"
ARCHIVE_DIR = "/mnt/data/killcore/archives"

ARCHIVE_LIMIT = 50  # 最多保留 50 名歷代王者

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
    archive_path = os.path.join(ARCHIVE_DIR, f"{new_king['name']}.json")
    save_json(archive_path, new_king)

    # 限制最多保留 ARCHIVE_LIMIT 個歷代王者
    all_archives = sorted(
        [f for f in os.listdir(ARCHIVE_DIR) if f.endswith(".json")],
        key=lambda x: os.path.getctime(os.path.join(ARCHIVE_DIR, x))
    )
    if len(all_archives) > ARCHIVE_LIMIT:
        os.remove(os.path.join(ARCHIVE_DIR, all_archives[0]))

def main():
    ranking = load_json(RANKING_PATH)
    if not ranking or not isinstance(ranking, list):
        print("[v09] 找不到有效排名資料")
        return

    new_king = ranking[0]
    current_king = load_json(KING_PATH)

    # 判斷是否是同一王者（以 name 為依據）
    if current_king.get("name") == new_king["name"]:
        new_king["king_count"] = current_king.get("king_count", 1) + 1
    else:
        new_king["king_count"] = 1

    save_json(KING_PATH, new_king)
    archive_king(new_king)

    # 清除非王者模組
    for fname in os.listdir(MODULE_DIR):
        if fname.endswith(".json") and fname != new_king["name"]:
            os.remove(os.path.join(MODULE_DIR, fname))

    print(f"[v09] 王者誕生：{new_king['name']}")
    print(f"[v09] 衛冕次數：{new_king['king_count']}")
    print(f"[v09] 已封存至：{KING_PATH}")

if __name__ == "__main__":
    main()
