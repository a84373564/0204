#!/usr/bin/env python3
# v16_eco_capital_allocator.py - 真實資金整合模擬分配器（封頂版）

import json
import os
import requests
import time
import hmac
import hashlib

KEY_PATH = "/mnt/data/killcore/mexc_keys.json"
KING_PATH = "/mnt/data/killcore/king_pool.json"
CAPITAL_PATH = "/mnt/data/killcore/allocated_capital.json"

MIN_CAPITAL = 50
MAX_CAPITAL = 1000

def load_keys():
    try:
        with open(KEY_PATH, "r") as f:
            keys = json.load(f)
        return keys["api_key"], keys["api_secret"]
    except:
        print("[v16] 無法載入 API 金鑰")
        return None, None

def fetch_wallet_balance():
    api_key, api_secret = load_keys()
    if not api_key or not api_secret:
        print("[v16] 金鑰缺失，使用 fallback 金額 1000 USDT")
        return 1000

    try:
        timestamp = str(int(time.time() * 1000))
        query = f"timestamp={timestamp}"
        signature = hmac.new(api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()
        url = f"https://api.mexc.com/api/v3/account?{query}&signature={signature}"
        headers = { "X-MEXC-APIKEY": api_key }

        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()

        for asset in data.get("balances", []):
            if asset.get("asset") == "USDT":
                return round(float(asset.get("free", 0)), 2)

    except Exception as e:
        print(f"[v16] API 錯誤，使用 fallback 金額：{e}")
    return 1000

def load_king():
    if not os.path.exists(KING_PATH):
        print("[v16] 找不到 king_pool.json")
        return None
    with open(KING_PATH, "r") as f:
        return json.load(f)

def allocate(mod, total):
    score = mod.get("score", 0)
    base = score * 10
    capital = min(max(base, MIN_CAPITAL), total, MAX_CAPITAL)
    return round(capital, 2)

def main():
    king = load_king()
    if not king:
        return

    total = fetch_wallet_balance()
    capital = allocate(king, total)

    result = {
        "module": king.get("name"),
        "symbol": king.get("symbol"),
        "strategy": king.get("strategy"),
        "score": king.get("score"),
        "allocated_capital": capital,
        "max_capital": MAX_CAPITAL,
        "min_capital": MIN_CAPITAL,
        "total_available": total,
        "source": "real_wallet" if total != 1000 else "fallback"
    }

    with open(CAPITAL_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[v16] 使用資金 {total} USDT，已分配給王者：{capital} USDT")
    print(f"[v16] 結果寫入：{CAPITAL_PATH}")

if __name__ == "__main__":
    main()
