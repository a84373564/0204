#!/usr/bin/env python3
# v03_binance_rank_evaluator.py - 使用 Binance API 替代 MEXC
import os, json, requests

POOL_PATH = "/mnt/data/killcore/symbol_pool.json"
OUTPUT_PATH = "/mnt/data/killcore/symbol_rank.json"
API_URL = "https://api.binance.com/api/v3/klines"
TIMEFRAME = "1h"
LIMIT = 24

def is_float(val):
    try:
        float(val)
        return True
    except:
        return False

def fetch_volatility(symbol):
    try:
        url = f"{API_URL}?symbol={symbol}&interval={TIMEFRAME}&limit={LIMIT}"
        resp = requests.get(url, timeout=10)
        data = resp.json()

        if not isinstance(data, list) or len(data) < 2:
            raise ValueError("無法取得合法 KLine")

        highs = [float(k[2]) for k in data if is_float(k[2])]
        lows = [float(k[3]) for k in data if is_float(k[3])]
        open_price = float(data[0][1]) if is_float(data[0][1]) else None

        if not highs or not lows or open_price is None:
            raise ValueError("數據不足或格式錯誤")

        volatility = (max(highs) - min(lows)) / open_price
        return round(volatility, 5)
    except Exception as e:
        print(f"[錯誤] {symbol} 波動失敗：{e}")
        return 0

def main():
    if not os.path.exists(POOL_PATH):
        print("[v03] 未找到 symbol_pool.json")
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
