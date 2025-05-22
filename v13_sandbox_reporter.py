# v13_sandbox_reporter.py（重構版）｜唯一王者損益分析報告
import json
import os
import matplotlib.pyplot as plt

king_path = "/mnt/data/killcore/king_pool.json"
summary_txt = "/mnt/data/killcore/king_summary.txt"
equity_chart = "/mnt/data/killcore/king_equity_curve.png"

if not os.path.exists(king_path):
    print("[v13] 找不到王者資料。")
    exit()

with open(king_path, "r") as f:
    king = json.load(f)

# 基礎資訊
name = king.get("name", "?")
symbol = king.get("symbol", "?")
score = king.get("score", 0)
profit = king.get("profit", 0)
win_rate = king.get("win_rate", 0)
sharpe = king.get("sharpe", 0)
drawdown = king.get("drawdown", 0)
strategy = king.get("strategy", "?")
rounds = king.get("survival_rounds", "?")

# 分析語句
status = "建議觀察"
if profit > 10 and sharpe > 2 and drawdown < 2:
    status = "可考慮實戰（建議低倉位）"
elif profit < 0 or sharpe < 1 or drawdown > 5:
    status = "風險過高，不建議實單"

# 寫入報告
with open(summary_txt, "w") as f:
    f.write(f"【現任王者分析報告】\n")
    f.write(f"模組名稱：{name}\n")
    f.write(f"幣別：{symbol}\n")
    f.write(f"策略類型：{strategy}\n")
    f.write(f"王者衛冕輪次：{rounds}\n")
    f.write(f"總分：{score:.2f}\n")
    f.write(f"獲利：{profit:.2f}\n")
    f.write(f"勝率：{win_rate:.2%}\n")
    f.write(f"Sharpe：{sharpe:.2f}\n")
    f.write(f"Drawdown：{drawdown:.2f}\n")
    f.write(f"實戰建議：{status}\n")

# 畫出損益曲線
log = king.get("log", [])
capital = 100
curve = []
for entry in log:
    if isinstance(entry, dict):
        capital += entry.get("pnl", 0)
        curve.append(capital)

if curve:
    plt.figure(figsize=(10, 4))
    plt.plot(curve, color="blue", marker='o')
    plt.title("王者模組損益曲線")
    plt.xlabel("模擬次數")
    plt.ylabel("資金變化")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(equity_chart)
    print(f"[v13] 損益圖已輸出：{equity_chart}")
else:
    print("[v13] 無法產生損益圖，模擬 log 缺失")

print(f"[v13] 報告已輸出：{summary_txt}")
