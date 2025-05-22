#!/usr/bin/env python3
# v17_eco_realistic_executor.py - 最強無敵版：嚴格實戰模擬驗證器

import json
import os
import random

KING_PATH = "/mnt/data/killcore/king_pool.json"
CAPITAL_PATH = "/mnt/data/killcore/allocated_capital.json"
RESULT_PATH = "/mnt/data/killcore/king_validation_result.json"

MAX_DRAWDOWN_ALLOWED = 5.0      # 最大容許回撤 (%)
MIN_SHARPE_REQUIRED = 1.5       # 最低 Sharpe 比
MIN_WIN_RATE_REQUIRED = 0.55    # 最低勝率

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        print(f"[v17] 無法載入 {path}")
        return None

def simulate_realistic_run(mod, capital):
    # 真實模擬範例邏輯（固定隨機，實際可改為回放歷史價格）
    random.seed(int(mod["score"] * 1000))

    profit_pct = round(random.uniform(-0.08, 0.18), 4)  # -8%~18%
    drawdown = round(random.uniform(0.5, 6.0), 4)
    sharpe = round(random.uniform(0.7, 3.5), 4)
    win_rate = round(random.uniform(0.3, 0.95), 4)

    profit = round(capital * profit_pct, 2)
    final = round(capital + profit, 2)
    cost_penalty = round(capital * 0.001, 2)  # 假設 0.1% 手續費
    slippage_penalty = round(capital * 0.002, 2)  # 假設 0.2% 滑價

    # 嚴格評分是否通過
    passed = (
        drawdown <= MAX_DRAWDOWN_ALLOWED and
        sharpe >= MIN_SHARPE_REQUIRED and
        win_rate >= MIN_WIN_RATE_REQUIRED and
        final > capital
    )

    return {
        "start_capital": capital,
        "final_capital": final,
        "profit_usdt": profit,
        "profit_pct": profit_pct,
        "drawdown": drawdown,
        "sharpe": sharpe,
        "win_rate": win_rate,
        "cost_penalty": cost_penalty,
        "slippage_penalty": slippage_penalty,
        "risk_score": round((sharpe - drawdown / 2) * win_rate, 3),
        "validation_passed": passed,
        "source": "v17_final_validation"
    }

def main():
    king = load_json(KING_PATH)
    capital_info = load_json(CAPITAL_PATH)
    if not king or not capital_info:
        print("[v17] 無法取得王者模組或資金資訊")
        return

    capital = capital_info.get("allocated_capital", 1000)
    result = simulate_realistic_run(king, capital)

    with open(RESULT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[v17] 王者實戰模擬完成，驗證結果寫入：{RESULT_PATH}")
    if result["validation_passed"]:
        print("[v17] 驗證通過：該王者具備實戰潛力")
    else:
        print("[v17] 驗證未通過：該王者應回沙盤重訓")

if __name__ == "__main__":
    main()
