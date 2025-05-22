#!/usr/bin/env python3
# v16_eco_capital_allocator.py - 使用真實錢包資金作為模擬上限分配資金

import json
import os
import requests

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
        return 1000  # fallback 模擬資金

    try:
        headers = {
            "Content-Type": "application/json",
            "ApiKey": api_key
        }
        url = "https://api.mexc.com/api/v3/account"
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        for asset in data.get("balances", []):
            if asset.get("asset") == "USDT":
                free = float(asset.get("free", 0))
                return round(free, 2)
    except Exception as e:
        print(f"[v16] 錢包查詢失敗，使用模擬資金：{e}")
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
        "total_available": total
    }

    with open(CAPITAL_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[v16] 使用錢包資金 {total} USDT，為王者分配：{capital} USDT")
    print(f"[v16] 資訊寫入：{CAPITAL_PATH}")

if __name__ == "__main__":
    main()
