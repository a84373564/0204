#!/usr/bin/env python3
# v07_sandbox_engine.py - 含成本統計（cost_penalty）最終版

import os, json, random

MODULE_DIR = "/mnt/data/killcore/modules"
PRICE_PATH = "/mnt/data/killcore/price_simulations.json"

FEE_RATE = 0.001  # 每次進出各 0.1%
SLIPPAGE_RANGE = (-0.001, 0.001)  # ±0.1% 隨機滑價

def simulate(prices, params):
    capital = 100
    wins = 0
    losses = 0
    equity = [capital]
    total_cost = 0

    for i in range(1, len(prices)):
        entry = prices[i - 1]
        slippage = random.uniform(*SLIPPAGE_RANGE)
        exit = prices[i] * (1 + slippage)

        fee = abs(entry * FEE_RATE + exit * FEE_RATE)
        total_cost += fee

        if exit > entry:
            profit = capital * 0.01 - fee
            wins += 1
        else:
            profit = -capital * 0.005 - fee
            losses += 1

        capital += profit
        equity.append(capital)

    total_return = round(equity[-1] - 100, 2)
    max_drawdown = round(min(equity) - 100, 2)
    sharpe = round((total_return / abs(max_drawdown + 0.01)), 2)
    win_rate = round(wins / (wins + losses + 1e-6), 4)

    return {
        "profit": total_return,
        "drawdown": abs(max_drawdown),
        "sharpe": sharpe,
        "win_rate": win_rate,
        "cost_penalty": round(total_cost, 4)
    }

def run_simulation(module_path, prices):
    with open(module_path, "r") as f:
        mod = json.load(f)

    sym = mod.get("symbol", "BTCUSDT")
    result = {}

    if sym not in prices:
        print(f"[跳過] 缺少價格資料：{sym}")
        return

    for scenario, data in prices[sym].items():
        result[scenario] = simulate(data, mod.get("params", {}))

    avg_profit = sum(r["profit"] for r in result.values()) / 4
    avg_drawdown = sum(r["drawdown"] for r in result.values()) / 4
    avg_sharpe = sum(r["sharpe"] for r in result.values()) / 4
    avg_win = sum(r["win_rate"] for r in result.values()) / 4
    avg_cost = sum(r["cost_penalty"] for r in result.values()) / 4

    mod.update({
        "simulations": result,
        "score": round(avg_profit - avg_drawdown * 5 + avg_sharpe * 3 + avg_win * 2, 2),
        "metrics": {
            "avg_profit": round(avg_profit, 2),
            "avg_drawdown": round(avg_drawdown, 2),
            "avg_sharpe": round(avg_sharpe, 2),
            "avg_win_rate": round(avg_win, 4),
            "avg_cost_penalty": round(avg_cost, 4)
        }
    })

    with open(module_path, "w") as f:
        json.dump(mod, f, indent=2)

def main():
    if not os.path.exists(PRICE_PATH):
        print("[v07] 價格資料不存在，請先執行 v06")
        return

    with open(PRICE_PATH, "r") as f:
        prices = json.load(f)

    files = [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]
    for fname in files:
        path = os.path.join(MODULE_DIR, fname)
        run_simulation(path, prices)

    print(f"[v07] 模組沙盤模擬完成（含成本統計）：{len(files)} 支")

if __name__ == "__main__":
    main()
