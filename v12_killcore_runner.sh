#!/bin/bash
# v12_killcore_runner.sh - Killcore 自動掛機巡邏流程（封頂防呆版）

LOCKFILE="/tmp/killcore_runner.lock"
LOGFILE="/mnt/data/killcore/killcore_runner.log"
STAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 防止重複執行
if [ -f "$LOCKFILE" ]; then
  echo "[v12][$STAMP] 已有掛機執行中，退出" >> "$LOGFILE"
  exit 1
fi
touch "$LOCKFILE"

echo "========== [v12] Killcore 巡邏啟動：$STAMP ==========" >> "$LOGFILE"

# 流程階段一：前置清理與選幣建構
python3 /mnt/data/killcore/v01_auto_schema_guard.py >> "$LOGFILE" 2>&1
python3 /mnt/data/killcore/v20_module_integrity_checker.py >> "$LOGFILE" 2>&1
python3 /mnt/data/killcore/v02_symbol_pool_builder.py >> "$LOGFILE" 2>&1
python3 /mnt/data/killcore/v03_symbol_rank_evaluator.py >> "$LOGFILE" 2>&1
python3 /mnt/data/killcore/v04_dead_symbol_filter.py >> "$LOGFILE" 2>&1

# 流程階段二：模組生成與沙盤競爭
python3 /mnt/data/killcore/v05_strategy_generator.py >> "$LOGFILE" 2>&1
python3 /mnt/data/killcore/v06_price_generator.py >> "$LOGFILE" 2>&1
python3 /mnt/data/killcore/v07_sandbox_engine.py >> "$LOGFILE" 2>&1
python3 /mnt/data/killcore/v08_evaluation_ruleset.py >> "$LOGFILE" 2>&1
python3 /mnt/data/killcore/v09_core_engine.py >> "$LOGFILE" 2>&1
python3 /mnt/data/killcore/v10_memory_bank.py >> "$LOGFILE" 2>&1
python3 /mnt/data/killcore/v11_king_pool.py >> "$LOGFILE" 2>&1

# 流程階段三：模擬實戰與風控準備
python3 /mnt/data/killcore/v16_eco_capital_allocator.py >> "$LOGFILE" 2>&1
python3 /mnt/data/killcore/v17_eco_realistic_executor.py >> "$LOGFILE" 2>&1
python3 /mnt/data/killcore/v18_eco_real_wallet_checker.py >> "$LOGFILE" 2>&1
python3 /mnt/data/killcore/v19_eco_live_trading_switch.py >> "$LOGFILE" 2>&1

# 流程階段四：尾段結構防爆再掃一次
python3 /mnt/data/killcore/v20_module_integrity_checker.py >> "$LOGFILE" 2>&1

echo "[v12][$STAMP] Killcore 巡邏結束" >> "$LOGFILE"
rm -f "$LOCKFILE"
