import json
from pathlib import Path

KING_PATH = Path("/mnt/data/killcore/king_pool.json")
CAPITAL_PATH = Path("/mnt/data/killcore/allocated_capital.json")
VALIDATION_PATH = Path("/mnt/data/killcore/king_validation_result.json")
SUMMARY_PATH = Path("/mnt/data/killcore/king_summary.txt")

def load_json(path):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}

def write_report(king, capital, final):
    lines = []
    lines.append("[ 王者資訊報表 v13.1 - summary only ]\n")
    lines.append(f"模組名稱：{king.get('name')}")
    lines.append(f"幣別：{king.get('symbol')}")
    lines.append(f"策略類型：{king.get('strategy')}")
    lines.append(f"總分：{king.get('score')}\n")

    metrics = king.get("metrics", {})
    lines.append("平均績效：")
    lines.append(f"- 平均獲利：{metrics.get('avg_profit', 'N/A')}")
    lines.append(f"- 平均回撤：{metrics.get('avg_drawdown', 'N/A')}")
    lines.append(f"- 平均勝率：{metrics.get('avg_win_rate', 'N/A')}")
    lines.append(f"- 平均 Sharpe：{metrics.get('avg_sharpe', 'N/A')}\n")

    lines.append("資金配置：")
    lines.append(f"- 配置資金：{capital.get('allocated_capital', 'N/A')} USDT")
    lines.append(f"- 可用總資金：{capital.get('total_available', 'N/A')} USDT")
    lines.append(f"- 來源：{capital.get('source', 'N/A')}\n")

    lines.append("實戰沙盤：")
    lines.append(f"- Profit：{final.get('profit_usdt', 'N/A')}")
    lines.append(f"- Drawdown：{final.get('drawdown', 'N/A')}")
    lines.append(f"- Sharpe：{final.get('sharpe', 'N/A')}")
    lines.append(f"- Win rate：{final.get('win_rate', 'N/A')}\n")
    lines.append("=== 結束 ===")

    result = "\n".join(lines)
    print(result)

    with open(SUMMARY_PATH, "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    king = load_json(KING_PATH)
    capital = load_json(CAPITAL_PATH)
    final = load_json(VALIDATION_PATH)

    write_report(king, capital, final)
    print(f"[v13] 王者報表完成，儲存於：{SUMMARY_PATH}")
