#!/usr/bin/env python3
# v18_eco_real_wallet_checker.py - 真實 MEXC 錢包資產監控器（USDT 餘額＋異常提示）

import json
import requests
import os
import time
import hmac
import hashlib

KEY_PATH = "/mnt/data/killcore/mexc_keys.json"
OUTPUT_PATH = "/mnt/data/killcore/wallet_snapshot.json"

def load_keys():
    try:
        with open(KEY_PATH, "r") as f:
            keys = json.load(f)
        return keys["api_key"], keys["api_secret"]
    except:
        print("[v18] 無法讀取 API 金鑰")
        return None, None

def get_wallet_snapshot():
    api_key, api_secret = load_keys()
    if not api_key or not api_secret:
        return { "error": "missing_keys", "usdt_balance": 0 }

    try:
        timestamp = str(int(time.time() * 1000))
        query = f"timestamp={timestamp}"
        signature = hmac.new(api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()
        url = f"https://api.mexc.com/api/v3/account?{query}&signature={signature}"
        headers = { "X-MEXC-APIKEY": api_key }

        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()

        snapshot = {
            "timestamp": timestamp,
            "assets": {},
            "usdt_balance": 0,
            "status": "ok"
        }

        for asset in data.get("balances", []):
            symbol = asset["asset"]
            free = float(asset.get("free", 0))
            locked = float(asset.get("locked", 0))
            total = round(free + locked, 4)

            if total > 0:
                snapshot["assets"][symbol] = {
                    "free": free,
                    "locked": locked,
                    "total": total
                }

            if symbol == "USDT":
                snapshot["usdt_balance"] = free

        return snapshot

    except Exception as e:
        print(f"[v18] API 查詢錯誤：{e}")
        return { "error": str(e), "usdt_balance": 0 }

def main():
    snapshot = get_wallet_snapshot()
    with open(OUTPUT_PATH, "w") as f:
        json.dump(snapshot, f, indent=2)
    print(f"[v18] 錢包狀態已寫入：{OUTPUT_PATH}")
    print(f"[v18] USDT 可用餘額：{snapshot.get('usdt_balance')}")

if __name__ == "__main__":
    main()
