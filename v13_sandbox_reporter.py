#!/usr/bin/env python3
import json
from pathlib import Path

KING_POOL_PATH = "/mnt/data/killcore/king_pool.json"
CAPITAL_PATH = "/mnt/data/killcore/allocated_capital.json"
VALIDATION_PATH = "/mnt/data/killcore/king_validation_result.json"
OUTPUT_PATH = "/mnt/data/killcore/king_summary.txt"

def load_json(path):
    if not Path(path).exists():
        return None
    with open(path, "r") as f:
        return json.load(f)

def write_report(king, capital_info, validation):
    with open(OUTPUT_PATH, "w") as f:
        f.write("[ 王者資訊報表 v13.1 - summary only ]\n\n")
        f.write(f"模組名稱: {king.get('name', 'N/A')}\n")
        f.write(f"幣別: {king.get('symbol', 'N/A')}\n")
        f.write(f"策略類型: {king.get('strategy', 'N/A')}\n")
        f.write(f"總得分: {king.get('score', 'N/A')}\n\n")

        f.write("平均績效:\n")
        metrics = king.get("metrics", {})
        f.write(f"- 平均獲利: {metrics.get('avg_profit', 'N/A')}\n")
        f.write(f"- 平均回撤: {metrics.get('avg_drawdown', 'N/A')}\n")
        f.write(f"- 平均勝率: {metrics.get('avg_win_rate', 'N/A')}\n")
        f.write(f"- 平均 Sharpe: {metrics.get('avg_sharpe', 'N/A')}\n\n")

        f.write("資金配置:\n")
        if capital_info:
            f.write(f"- 配置資金: {capital_info.get('allocated_capital', 'N/A')} USDT\n")
            f.write(f"- 可用總資金: {capital_info.get('total_available', 'N/A')} USDT\n")
            f.write(f"- 來源: {capital_info.get('source', 'N/A')}\n\n")
        else:
            f.write("- 資訊缺失\n\n")

        f.write("實戰沙盤:\n")
        if validation:
            f.write(f"- Profit: {validation.get('profit_usdt', 'N/A')}\n")
            f.write(f"- Drawdown: {validation.get('drawdown', 'N/A')}\n")
            f.write(f"- Sharpe: {validation.get('sharpe', 'N/A')}\n")
            f.write(f"- Win rate: {validation.get('win_rate', 'N/A')}\n")
        else:
            f.write("- 尚未模擬或缺少驗證資料\n")

        f.write("\n=== 結束 ===\n")

def main():
    king_data = load_json(KING_POOL_PATH)
    if not king_data:
        print("[v13] 找不到王者模組資料")
        return

    capital_info = load_json(CAPITAL_PATH)
    validation_info = load_json(VALIDATION_PATH)

    king = king_data if isinstance(king_data, dict) else king_data[0]
    write_report(king, capital_info, validation_info)
    print(f"[v13] 王者報表完成，儲存於：{OUTPUT_PATH}")

if __name__ == "__main__":
    main()
