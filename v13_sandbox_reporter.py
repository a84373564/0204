# v13_sandbox_reporter.py
# 功能：讀取 round_log.jsonl 並產生圖表與統計報表
import json
import pandas as pd
import matplotlib.pyplot as plt
import os

ROUND_LOG_PATH = "/mnt/data/killcore/round_log.jsonl"
SCORE_TREND_PATH = "/mnt/data/killcore/v13_score_trend.png"
SYMBOL_TOP10_PATH = "/mnt/data/killcore/v13_symbol_top10.png"

def load_round_logs(path):
    if not os.path.exists(path):
        print(f"[v13] 找不到資料：{path}")
        return []
    with open(path, "r") as f:
        return [json.loads(line.strip()) for line in f]

def generate_score_chart(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df["round"], df["score"], marker="o", linestyle="-")
    plt.title("王者分數演化趨勢")
    plt.xlabel("巡邏輪次")
    plt.ylabel("總分")
    plt.grid(True)
    plt.savefig(SCORE_TREND_PATH)
    plt.close()
    print(f"[v13] 分數趨勢圖儲存至：{SCORE_TREND_PATH}")

def generate_symbol_chart(df):
    plt.figure(figsize=(10, 5))
    df["symbol"].value_counts().head(10).plot(kind="bar", color="skyblue")
    plt.title("王者幣別出現頻率 Top 10")
    plt.xlabel("幣別")
    plt.ylabel("出現次數")
    plt.tight_layout()
    plt.savefig(SYMBOL_TOP10_PATH)
    plt.close()
    print(f"[v13] 幣別分布圖儲存至：{SYMBOL_TOP10_PATH}")

def main():
    data = load_round_logs(ROUND_LOG_PATH)
    if not data:
        return
    df = pd.DataFrame(data).sort_values("round").reset_index(drop=True)
    generate_score_chart(df)
    generate_symbol_chart(df)
    print(f"[v13] 已完成王者輪次報表產出，共 {len(df)} 輪")

if __name__ == "__main__":
    main()
