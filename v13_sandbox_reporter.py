# v13_sandbox_reporter.py
# 王者沙盤實力報表 v13.3 - summary only

import json
from datetime import datetime

KING_SUMMARY_PATH = "/mnt/data/killcore/king_summary.txt"
VALIDATION_PATH = "/mnt/data/killcore/king_validation_result.json"
CAPITAL_PATH = "/mnt/data/killcore/allocated_capital.json"
HISTORY_PATH = "/mnt/data/killcore/king_archive.json"
KING_POOL_PATH = "/mnt/data/killcore/king_pool.json"

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def write_report(king, val, capital, history):
    with open(KING_SUMMARY_PATH, "w") as f:
        f.write("[ 王者資訊報表 v13.3 - summary only ]\n\n")
        f.write(f"模組名稱: {king.get('name')}\n")
        f.write(f"幣別: {king.get('symbol')}\n")
        f.write(f"策略類型: {king.get('strategy')}\n")
        f.write(f"總分: {king.get('score')}\n")

        f.write("\n平均績效:\n")
        f.write(f" - 平均獲利: {king.get('avg_profit')}\n")
        f.write(f" - 平均回撤: {king.get('avg_drawdown')}\n")
        f.write(f" - 平均勝率: {king.get('avg_win_rate')}\n")
        f.write(f" - 平均 Sharpe: {king.get('avg_sharpe')}\n")

        f.write("\n資金配置:\n")
        f.write(f" - 配置資金: {capital.get('allocated_capital', 'N/A')} USDT\n")
        f.write(f" - 可用總資金: {capital.get('total_available', 'N/A')} USDT\n")
        f.write(f" - 來源: {capital.get('source', 'unknown')}\n")

        f.write("\n實戰沙盤:\n")
        f.write(f" - Profit: {val.get('profit_usdt', 'N/A')}\n")
        f.write(f" - Drawdown: {val.get('drawdown', 'N/A')}\n")
        f.write(f" - Sharpe: {val.get('sharpe', 'N/A')}\n")
        f.write(f" - Win rate: {val.get('win_rate', 'N/A')}\n")

        f.write("\n血統資訊:\n")
        f.write(f" - 是否為重生者: {str(king.get('from_retry', False))}\n")
        f.write(f" - 衛冕次數: {king.get('defend_count', 0)} 次\n")

        if isinstance(history, list):
            f.write("\n歷代前五名紀錄:\n")
            top_kings = sorted(history, key=lambda x: x.get("score", 0), reverse=True)[:5]
            for k in top_kings:
                f.write(f" - {k.get('name')} / {k.get('symbol')} / score={k.get('score')}\n")

        f.write("\n=== 結束 ===\n")

def main():
    king_data = load_json(KING_POOL_PATH)
    val_data = load_json(VALIDATION_PATH)
    cap_data = load_json(CAPITAL_PATH)
    hist_data = load_json(HISTORY_PATH)

    if king_data:
        write_report(king_data, val_data, cap_data, hist_data)
        print(f"[v13] 王者報表完成，儲存於：{KING_SUMMARY_PATH}")
    else:
        print("[v13] 無法產生報表，模組資料不存在")

if __name__ == "__main__":
    main()
