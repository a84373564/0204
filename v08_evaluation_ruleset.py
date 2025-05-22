#!/usr/bin/env python3
# v08_evaluation_ruleset.py - 無敵版多因子評分器，支援排序、錯誤偵測、排行榜導出

import os, json

MODULE_DIR = "/mnt/data/killcore/modules"
RANKING_PATH = "/mnt/data/killcore/module_ranking.json"
TOP_PATH = "/mnt/data/killcore/top_candidate.json"
LOG_PATH = "/mnt/data/killcore/evaluation_log.txt"

# 欄位權重設定（可調整）
WEIGHTS = {
    "avg_profit": 1.5,
    "avg_drawdown": -3,
    "avg_sharpe": 2,
    "avg_win_rate": 2,
    "avg_cost_penalty": -2,
    "risk_reward_ratio": 1.5,
    "strategy_accuracy": 3,
    "profit_stability": -1,
    "realistic_final_capital": 0.5
}

def calculate_score(metrics):
    score = 0
    for key, weight in WEIGHTS.items():
        if key in metrics:
            score += metrics[key] * weight
    return round(score, 4)

def main():
    modules = []
    errors = []

    for fname in os.listdir(MODULE_DIR):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(MODULE_DIR, fname)
        try:
            with open(path, "r") as f:
                mod = json.load(f)

            metrics = mod.get("metrics", {})
            score = calculate_score(metrics)
            mod["score"] = score

            with open(path, "w") as f:
                json.dump(mod, f, indent=2)

            modules.append({
                "name": mod.get("name", fname),
                "score": score,
                "symbol": mod.get("symbol"),
                "strategy": mod.get("strategy"),
                "metrics": metrics
            })

        except Exception as e:
            errors.append(f"{fname}: {str(e)}")

    modules.sort(key=lambda x: x["score"], reverse=True)

    with open(RANKING_PATH, "w") as f:
        json.dump(modules, f, indent=2)

    if modules:
        with open(TOP_PATH, "w") as f:
            json.dump(modules[0], f, indent=2)

    with open(LOG_PATH, "w") as f:
        f.write(f"[v08] 評分完成，共計模組：{len(modules)}，錯誤：{len(errors)}\\n")
        for err in errors:
            f.write(f"錯誤模組：{err}\\n")

    print(f"[v08] 評分完成，排名已寫入：{RANKING_PATH}")
    print(f"[v08] 王者候選已輸出：{TOP_PATH}")
    if errors:
        print(f"[v08] 錯誤模組記錄於：{LOG_PATH}")

if __name__ == "__main__":
    main()
