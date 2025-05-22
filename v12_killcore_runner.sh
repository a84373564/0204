#!/bin/bash
# v12.4 - Killcore 巡邏主控腳本｜含防呆鎖、輪次記錄、穩定巡邏

LOCKFILE="/tmp/killcore_runner.lock"
ROUND_FILE="/mnt/data/killcore/round_counter.txt"

# 防止重複執行
if [ -f "$LOCKFILE" ]; then
  echo "[v12.4][$(date '+%Y-%m-%d %H:%M:%S')] 檢測到執行中，退出..."
  exit 1
fi
touch "$LOCKFILE"

# 初始化輪次
if [ ! -f "$ROUND_FILE" ]; then
  echo "1" > "$ROUND_FILE"
fi

while true; do
  STAMP=$(date '+%Y-%m-%d %H:%M:%S')
  ROUND=$(cat "$ROUND_FILE")
  echo "[v12.4][$STAMP] === 第 $ROUND 輪 巡邏開始 ==="

  MODULES=(
    "v01_auto_schema_guard.py"
    "v02_symbol_pool_builder.py"
    "v03_symbol_rank_evaluator.py"
    "v04_dead_symbol_filter.py"
    "v05_strategy_generator.py"
    "v06_price_generator.py"
    "v07_sandbox_engine.py"
    "v08_evaluation_ruleset.py"
    "v09_core_engine.py"
    "v10_memory_bank.py"
    "v11_king_pool.py"
    "v14_king_archive.py"
    "v16_eco_capital_allocator.py"
    "v17_eco_realistic_executor.py"
    "v18_eco_real_wallet_checker.py"
    "v19_eco_live_trading_switch.py"
    "v20_module_integrity_checker.py"
  )

  for MODULE in "${MODULES[@]}"; do
    echo "[v12.4][$STAMP] 執行中：$MODULE"
    python3 "/mnt/data/killcore/$MODULE"
  done

  echo "[v12.4][$STAMP] 第 $ROUND 輪 巡邏完成"
  NEXT=$((ROUND + 1))
  echo "$NEXT" > "$ROUND_FILE"

  echo "[v12.4] 等待 30 秒後進入第 $NEXT 輪..."
  sleep 30
done
