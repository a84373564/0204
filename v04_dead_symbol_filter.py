#!/usr/bin/env python3
# v04_dead_symbol_filter.py - 黑名單＋死幣過濾器（無敵版）

import os, json

POOL_PATH = "/mnt/data/killcore/symbol_pool.json"
OUTPUT_PATH = "/mnt/data/killcore/symbol_filtered.json"

# 可擴充黑名單
BLACKLIST = [
    "BELUGAUSDT", "LUNCUSDT", "PEPEUSDT", "1000SHIBUSDT",
    "SUDOUSDT", "BITCOINABCUSDT"
]

# 濾掉有這些關鍵字的幣（通常是槓桿或 ETF）
FORBIDDEN_KEYWORDS = ["3L", "3S", "5L", "5S", "DOWN", "UP", "ETF", "_"]

def is_valid_symbol(symbol):
    if symbol in BLACKLIST:
        return False
    if not symbol.endswith("USDT"):
        return False
    if any(kw in symbol for kw in FORBIDDEN_KEYWORDS):
        return False
    return True

def main():
    if not os.path.exists(POOL_PATH):
        print("[v04] 找不到 symbol_pool.json，請先執行 v02")
        return

    with open(POOL_PATH, "r") as f:
        symbols = json.load(f)

    filtered = [sym for sym in symbols if is_valid_symbol(sym)]

    with open(OUTPUT_PATH, "w") as f:
        json.dump(filtered, f, indent=2)

    print(f"[v04] 有效幣種保留：{filtered}")

if __name__ == "__main__":
    main()
