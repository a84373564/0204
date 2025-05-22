#!/usr/bin/env python3
# v07_sandbox_engine.py - 無敵模擬器：含13項實戰指標（風險、穩定、報酬、預測力）

import os, json, random

MODULE_DIR = "/mnt/data/killcore/modules"
PRICE_PATH = "/mnt/data/killcore/price_simulations.json"

FEE_RATE = 0.001
SLIPPAGE_RANGE = (-0.001, 0.001)

def simulate(prices, params):
    capital = 100
    wins = 0
    losses = 0
    equity = [capital]
    total_cost = 0
    correct_direction = 0
    total_trades = 0
    total_gain = 0
    total_loss = 0
    trade_returns = []
    max_consec_win = 0
    max_consec_loss = 0
    cur_win = 0
    cur_loss = 0

    for i in range(1, len(prices)):
        entry = prices[i - 1]
        slippage = random.uniform(*SLIPPAGE_RANGE)
        exit = prices[i] * (1 + slippage)
        fee = abs(entry * FEE_RATE + exit * FEE_RATE)
        total_cost += fee

        delta = exit - entry
        result = 0

        if exit > entry:
            result = capital * 0.01 - fee
            wins += 1
            cur_win += 1
            cur_loss = 0
            correct_direction += 1
            total_gain += result
        else:
            result = -capital * 0.005 - fee
            losses += 1
            cur_loss += 1
            cur_win = 0
            total_loss += abs(result)

        capital += result
        equity.append(capital)
        trade_returns.append(result)
        total_trades += 1
        max_consec_win = max(max_consec_win, cur_win)
        max_consec_loss = max(max_consec_loss, cur_loss)

    final_capital = capital
    avg_return = sum(trade_returns) / (total_trades or 1)
    profit_std = (sum((x - avg_return) ** 2 for x in trade_returns) / (total_trades or 1)) ** 0.5
    profit_stability = round(profit_std / (abs(avg_return) + 1e-6), 4)
    risk_reward_ratio = round((total_gain / (total_loss + 1e-6)), 4)
    strategy_accuracy = round(correct_direction / (total_trades or 1), 4)
    total_return = round(equity[-1] - 100, 2)
    max_drawdown = round(min(equity) - 100, 2)
    sharpe = round((total_return / abs(max_drawdown + 0.01)), 2)
    win_rate = round(wins / (wins + losses + 1e-6), 4)

    return {
        "profit": total_return,
        "drawdown": abs(max_drawdown),
        "sharpe": sharpe,
        "win_rate": win_rate,
        "cost_penalty": round(total_cost, 4),
        "risk_reward_ratio": risk_reward_ratio,
        "strategy_accuracy": strategy_accuracy,
        "profit_stability": profit_stability,
        "max_consecutive_loss": max_consec_loss,
        "max_consecutive_win": max_consec_win,
        "realistic_final_capital": round(final_capital, 2),
        "average_trade_return": round(avg_return, 4)
    }

def run_simulation(module_path, prices, vol_dict):
    with open(module_path, "r") as f:
        mod = json.load(f)

    sym = mod.get("symbol", "BTCUSDT")
    result = {}

    if sym not in prices:
        print(f"[跳過] 缺少價格資料：{sym}")
        return

    for scenario, data in prices[sym].items():
        result[scenario] = simulate(data, mod.get("params", {}))

    metrics = {}
    keys = list(result["choppy"].keys())
    for k in keys:
        metrics[f"avg_{k}"] = round(sum(result[sc][k] for sc in result) / 4, 4)

    mod.update({
        "simulations": result,
        "score": round(metrics["avg_profit"] - metrics["avg_drawdown"] * 5 + metrics["avg_sharpe"] * 3 + metrics["avg_win_rate"] * 2, 2),
        "metrics": metrics
    })

    if sym in vol_dict:
        mod["metrics"]["volatility_score_used"] = vol_dict[sym]

    with open(module_path, "w") as f:
        json.dump(mod, f, indent=2)

def main():
    if not os.path.exists(PRICE_PATH):
        print("[v07] 缺少 price_simulations.json，請先執行 v06")
        return

    with open(PRICE_PATH, "r") as f:
        prices = json.load(f)

    # 自動推估該 symbol 的總波動率
    vol_dict = {}
    for sym in prices:
        all_prices = prices[sym]["choppy"] + prices[sym]["uptrend"] + prices[sym]["downtrend"] + prices[sym]["volatile"]
        vol_dict[sym] = round((max(all_prices) - min(all_prices)) / (all_prices[0] + 1e-6), 5)

    files = [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]
    for fname in files:
        path = os.path.join(MODULE_DIR, fname)
        run_simulation(path, prices, vol_dict)

    print(f"[v07] 模組沙盤模擬完成（無敵版｜13 欄位）：{len(files)} 支")

if __name__ == "__main__":
    main()
