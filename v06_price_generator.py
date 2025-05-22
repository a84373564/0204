#!/usr/bin/env python3
# v06_price_generator.py - 多情境價格模擬器（uptrend, downtrend, choppy, volatile）

import os, json, random

SYMBOLS_PATH = "/mnt/data/killcore/symbol_filtered.json"
OUTPUT_PATH = "/mnt/data/killcore/price_simulations.json"
DAYS = 100  # 每種情境產 100 根價格

def generate_choppy(base):
    return [round(base + random.uniform(-1, 1), 2) for _ in range(DAYS)]

def generate_uptrend(base):
    return [round(base * (1 + 0.001 * i + random.uniform(-0.002, 0.002)), 2) for i in range(DAYS)]

def generate_downtrend(base):
    return [round(base * (1 - 0.001 * i + random.uniform(-0.002, 0.002)), 2) for i in range(DAYS)]

def generate_volatile(base):
    price = base
    series = []
    for _ in range(DAYS):
        price += random.uniform(-0.05, 0.05) * base
        series.append(round(max(price, 0.1), 2))
    return series

def main():
    if not os.path.exists(SYMBOLS_PATH):
        print("[v06] 請先執行 v02，建立 symbol_filtered.json")
        return

    with open(SYMBOLS_PATH, "r") as f:
        symbols = json.load(f)

    simulations = {}
    for sym in symbols:
        base = random.uniform(10, 1000)
        simulations[sym] = {
            "choppy": generate_choppy(base),
            "uptrend": generate_uptrend(base),
            "downtrend": generate_downtrend(base),
            "volatile": generate_volatile(base)
        }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(simulations, f, indent=2)

    print(f"[v06] 已完成模擬價格建構：{list(simulations.keys())}")

if __name__ == "__main__":
    main()
