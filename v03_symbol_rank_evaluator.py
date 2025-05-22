#!/usr/bin/env python3
# v03_symbol_rank_evaluator.py - 修正完成穩定版
import os, json, requests

POOL_PATH = "/mnt/data/killcore/symbol_pool.json"
OUTPUT_PATH = "/mnt/data/killcore/symbol_rank.json"
API_URL = "https://api.mexc.com/api/v3/klines"
TIMEFRAME = "1h"
LIMIT = 24

def is_float(value):
    try:
        float(value)
        return True
    except:
        return False

def fetch_volatility(symbol):
    try:
        url = f"{API_URL}?symbol={symbol}&interval={TIMEFRAME}&limit={LIMIT}"
        resp = requests.get(url, timeout=10)
        kline = resp.json()
        
        highs = [float(k[2]) for k in kline if is_float(k[2])]
        lows = [float(k[3]) for k in kline if is_float(k[3])]
        open_price = float(kline[0][1]) if is_float(kline[0][1]) else None

        if not highs or not lows or open_price is None:
            raise ValueError("Kline 資料格式不完整")

        high = max(highs)
        low = min(lows)
        volatility = (high - low) / open_price
        return round(volatility, 5)
    except Exception as e:
        print(f"[錯誤] {symbol} 波動失敗：{e}")
        return 0

def main():
    if not os.path.exists(POOL_PATH):
        print("[v03] 找不到 symbol_pool.json，請先執行 v02")
        return

    with open(POOL_PATH, "r") as f:
        symbols = json.load(f)

    ranks = []
    for sym in symbols:
        score = fetch_volatility(sym)
        ranks.append({"symbol": sym, "volatility_score": score})

    ranks_sorted = sorted(ranks, key=lambda x: x["volatility_score"], reverse=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(ranks_sorted, f, indent=2)

    print(f"[v03] 排名完成：{[r['symbol'] for r in ranks_sorted]}")

if __name__ == "__main__":
    main()
