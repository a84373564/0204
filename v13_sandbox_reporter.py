# v13_sandbox_reporter.py
import json
from pathlib import Path

KING_POOL_PATH = "/mnt/data/killcore/king_pool.json"
CAPITAL_PATH = "/mnt/data/killcore/allocated_capital.json"
VALIDATION_PATH = "/mnt/data/killcore/king_validation_result.json"
SUMMARY_PATH = "/mnt/data/killcore/king_summary.txt"

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def write_summary(king, capital, validation):
    with open(SUMMARY_PATH, "w") as f:
        f.write("[ 王者資訊報表 v13.1 - summary only ]\n\n")
        f.write(f"模組名稱：{king.get('name', 'N/A')}\n")
        f.write(f"幣別：{king.get('symbol', 'N/A')}\n")
        f.write(f"策略類型：{king.get('strategy', 'N/A')}\n")
        f.write(f"總分：{king.get('score', 'N/A')}\n\n")

        f.write("平均績效：\n")
        metrics = king.get("metrics", {})
        f.write(f"  - 平均獲利：{metrics.get('avg_profit', 'N/A')}\n")
        f.write(f"  - 平均回撤：{metrics.get('avg_drawdown', 'N/A')}\n")
        f.write(f"  - 平均勝率：{metrics.get('avg_win_rate', 'N/A')}\n")
        f.write(f"  - 平均 Sharpe：{metrics.get('avg_sharpe', 'N/A')}\n\n")

        f.write("資金配置：\n")
        if capital:
            f.write(f"  - 配置資金：{capital.get('allocated_capital', 'N/A')} USDT\n")
            f.write(f"  - 可用總資金：{capital.get('total_available', 'N/A')} USDT\n")
            f.write(f"  - 來源：{capital.get('source', 'N/A')}\n\n")
        else:
            f.write("  - 無法讀取資金配置資訊\n\n")

        f.write("實戰沙盤：\n")
        if validation:
            f.write(f"  - Profit：{validation.get('profit', 'N/A')}\n")
            f.write(f"  - Drawdown：{validation.get('drawdown', 'N/A')}\n")
            f.write(f"  - Sharpe：{validation.get('sharpe', 'N/A')}\n")
            f.write(f"  - Win rate：{validation.get('win_rate', 'N/A')}\n")
        else:
            f.write("  - 無實戰模擬資料\n")

        f.write("\n=== 結束 ===\n")

def main():
    king_data = load_json(KING_POOL_PATH)
    king = king_data if isinstance(king_data, dict) else {}
    capital = load_json(CAPITAL_PATH)
    validation = load_json(VALIDATION_PATH)
    write_summary(king, capital, validation)
    print("[v13] 王者報表完成，儲存於：", SUMMARY_PATH)

if __name__ == "__main__":
    main()
