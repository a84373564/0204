#!/usr/bin/env python3
# v08_evaluation_ruleset.py - 模組評分器（最強穩定版本）

import os, json

MODULE_DIR = "/mnt/data/killcore/modules"
REQUIRED_KEYS = ["profit", "drawdown", "sharpe", "win_rate"]
SCORE_WEIGHTS = {
    "profit": 1.5,
    "drawdown": -1.2,
    "sharpe": 2.0,
    "win_rate": 1.0
}

def load_module(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[v08] 無法讀取 {path}：{e}")
        return None

def save_module(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def evaluate(mod):
    try:
        score = 0
        for key, weight in SCORE_WEIGHTS.items():
            value = mod.get(key)
            if value is None or not isinstance(value, (int, float)):
                raise ValueError(f"{key} 欄位缺失或類型錯誤：{value}")
            score += value * weight

        prev_score = mod.get("score")
        mod["score_delta"] = round(score - prev_score, 2) if isinstance(prev_score, (int, float)) else None
        mod["score"] = round(score, 3)
        return mod

    except Exception as e:
        mod["score_error"] = str(e)
        print(f"[v08] 評分失敗：{mod.get('name', '?')} → {e}")
        return mod

def main():
    files = [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]
    total = len(files)
    count = 0
    best_score = -999999
    best_name = None

    for fname in files:
        path = os.path.join(MODULE_DIR, fname)
        mod = load_module(path)
        if not mod:
            continue

        mod = evaluate(mod)
        save_module(path, mod)

        if isinstance(mod.get("score"), (int, float)) and mod["score"] > best_score:
            best_score = mod["score"]
            best_name = fname

        count += 1

    print(f"[v08] 評分完成，共 {count} 隻模組")
    if best_name:
        print(f"[v08] 最高分：{best_name} → 分數 {best_score}")

if __name__ == "__main__":
    main()
