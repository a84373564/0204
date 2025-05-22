#!/usr/bin/env python3
# v07_sandbox_engine.py - Killcore 沙盤模擬器（最強版，績效補齊）

import os, json
from datetime import datetime
import random

MODULE_DIR = "/mnt/data/killcore/modules"
REQUIRED_KEYS = ["profit", "drawdown", "sharpe", "win_rate"]

def simulate_performance():
    """產生模擬績效數據（可替換為實戰模擬器）"""
    profit = round(random.uniform(-5, 10), 2)
    drawdown = round(random.uniform(0.5, 5.0), 2)
    sharpe = round(profit / drawdown if drawdown else 0, 4)
    win_rate = round(random.uniform(0.3, 0.9), 4)
    return {
        "profit": profit,
        "drawdown": drawdown,
        "sharpe": sharpe,
        "win_rate": win_rate,
        "simulated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "simulated": True
    }

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    if not os.path.exists(MODULE_DIR):
        print("[v07] 模組資料夾不存在")
        return

    files = [f for f in os.listdir(MODULE_DIR) if f.endswith(".json")]
    total, patched = 0, 0

    for fname in files:
        fpath = os.path.join(MODULE_DIR, fname)
        mod = load_json(fpath)
        if not mod or not isinstance(mod, dict):
            continue

        if any(k not in mod for k in REQUIRED_KEYS):
            mod.update(simulate_performance())
            save_json(fpath, mod)
            patched += 1

        total += 1

    print(f"[v07] 共掃描 {total} 支模組，已補齊 {patched} 支績效欄位")

if __name__ == "__main__":
    main()
