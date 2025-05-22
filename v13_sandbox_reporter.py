import json
import os

REPORT_PATH = "/mnt/data/killcore/king_summary.txt"
KING_POOL_PATH = "/mnt/data/killcore/king_pool.json"
CAPITAL_PATH = "/mnt/data/killcore/allocated_capital.json"

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[x] 無法讀取 {path}: {e}")
        return None

def write_report(king):
    lines = []
    lines.append(f"王者名稱: {king.get('name', 'N/A')}")
    lines.append(f"幣種: {king.get('symbol', 'N/A')}")
    lines.append(f"策略: {king.get('strategy', 'N/A')}")
    lines.append(f"分數: {king.get('score', 'N/A')}")

    sim = king.get("simulations", {})
    lines.append("\n=== 模擬結果 ===")
    for scenario in ["choppy", "uptrend", "downtrend", "volatile"]:
        s = sim.get(scenario, {})
        lines.append(f"- {scenario}")
        lines.append(f"  獲利: {s.get('profit', 'N/A')}")
        lines.append(f"  回撤: {s.get('drawdown', 'N/A')}")
        lines.append(f"  勝率: {s.get('win_rate', 'N/A')}")
        lines.append(f"  Sharpe: {s.get('sharpe', 'N/A')}")

    metrics = king.get("metrics", {})
    lines.append("\n=== 總結指標 ===")
    lines.append(f"平均獲利: {metrics.get('avg_profit', 'N/A')}")
    lines.append(f"平均回撤: {metrics.get('avg_drawdown', 'N/A')}")
    lines.append(f"平均勝率: {metrics.get('avg_win_rate', 'N/A')}")
    lines.append(f"平均 Sharpe: {metrics.get('avg_sharpe', 'N/A')}")

    with open(REPORT_PATH, "w") as f:
        f.write("\n".join(lines))

def main():
    king_pool = load_json(KING_POOL_PATH)
    if not king_pool:
        print("[x] 找不到王者模組")
        return
    king = king_pool

    cap_info = load_json(CAPITAL_PATH)
    if cap_info:
        cap = cap_info.get("capital_allocation", {})
        king_usdt = cap.get(king["name"], "N/A")
        print(f"[v13] 實戰資金分配：{king_usdt} USDT")
    else:
        print("[v13] 無法取得資金資料")

    write_report(king)
    print(f"[v13] 王者報表完成，儲存於：{REPORT_PATH}")

if __name__ == "__main__":
    main()
