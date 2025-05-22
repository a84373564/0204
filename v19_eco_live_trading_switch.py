#!/usr/bin/env python3
# v19_eco_live_trading_switch.py - 是否開啟實單交易（最強無敵版控制器）

import json
import os

WALLET_PATH = "/mnt/data/killcore/wallet_snapshot.json"
VALIDATION_PATH = "/mnt/data/killcore/king_validation_result.json"
SWITCH_PATH = "/mnt/data/killcore/live_trading_switch.json"

REQUIRE_MIN_BALANCE = 100     # 最低資金門檻
REQUIRE_PASS_VALIDATION = True
RISK_THRESHOLD = 1.25          # 最低風控分數（risk_score）

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        print(f"[v19] 無法載入 {path}")
        return None

def decide_live_trading(wallet, validation):
    usdt = wallet.get("usdt_balance", 0)
    risk_score = validation.get("risk_score", 0)
    passed = validation.get("validation_passed", False)

    reasons = []
    if usdt < REQUIRE_MIN_BALANCE:
        reasons.append(f"資金不足 ({usdt} < {REQUIRE_MIN_BALANCE})")
    if REQUIRE_PASS_VALIDATION and not passed:
        reasons.append("模擬驗證未通過")
    if risk_score < RISK_THRESHOLD:
        reasons.append(f"風控分數過低 ({risk_score} < {RISK_THRESHOLD})")

    allow = len(reasons) == 0
    return {
        "live_trading_allowed": allow,
        "usdt_balance": usdt,
        "risk_score": risk_score,
        "validation_passed": passed,
        "reasons_blocked": reasons,
        "decision_by": "v19_live_trading_switch"
    }

def main():
    wallet = load_json(WALLET_PATH)
    validation = load_json(VALIDATION_PATH)

    if not wallet or not validation:
        print("[v19] 無法取得錢包或模擬資訊")
        return

    decision = decide_live_trading(wallet, validation)

    with open(SWITCH_PATH, "w") as f:
        json.dump(decision, f, indent=2)

    print(f"[v19] 是否開單決策結果已寫入：{SWITCH_PATH}")
    print(f"[v19] 狀態：{'允許實單' if decision['live_trading_allowed'] else '禁止實單'}")

if __name__ == "__main__":
    main()
