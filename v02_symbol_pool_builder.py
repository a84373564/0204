#!/usr/bin/env python3
# v02_symbol_pool_builder.py - 實戰無敵版
import os, json, requests

KEY_PATH = "/mnt/data/killcore/mexc_keys.json"
OUTPUT_PATH = "/mnt/data/killcore/symbol_pool.json"
API_URL = "https://api.mexc.com/api/v3/ticker/24hr"
TOP_LIMIT = 2
MIN_VOLUME_USDT = 5000000
CAPITAL_THRESHOLD = 100  # 排除下單門檻過高的幣，針對小資

def get_keys():
    try:
        with open(KEY_PATH, "r") as f:
            keys = json.load(f)
        return keys["api_key"], keys["api_secret"]
    except Exception as e:
        print(f"[!] 無法讀取金鑰：{e}")
        return None, None

def fetch_symbols():
    try:
        resp = requests.get(API_URL, timeout=10)
        data = resp.json()
        filtered = []
        for item in data:
            symbol = item.get("symbol", "")
            vol = float(item.get("quoteVolume", 0))
            if not symbol.endswith("USDT"):
                continue
            if any(x in symbol for x in ["3L", "3S", "5L", "5S", "DOWN", "UP", "ETF", "_"]):
                continue
            if vol < MIN_VOLUME_USDT:
                continue
            filtered.append((symbol, vol))
        sorted_syms = sorted(filtered, key=lambda x: x[1], reverse=True)
        return [s[0] for s in sorted_syms[:TOP_LIMIT]]
    except Exception as e:
        print(f"[錯誤] 無法取得幣種資料：{e}")
        return []

def main():
    api_key, api_secret = get_keys()
    if not api_key:
        print("[v02] 金鑰錯誤，無法繼續")
        return

    symbols = fetch_symbols()
    if symbols:
        with open(OUTPUT_PATH, "w") as f:
            json.dump(symbols, f, indent=2)
        print(f"[v02] 幣池建構成功：{symbols}")
    else:
        print("[v02] 幣池建構失敗，請檢查網路或資金狀況")

if __name__ == "__main__":
    main()
