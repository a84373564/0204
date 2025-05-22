#!/bin/bash
# v12.2 Killcore 巡邏強化版：支援輪次統計、王者歷史記錄、即時輸出

LOCKFILE="/tmp/killcore_runner.lock"
LOGFILE="/mnt/data/killcore/killcore_runner.log"
ROUND_FILE="/mnt/data/killcore/round_counter.txt"
ROUND_LOG="/mnt/data/killcore/round_log.jsonl"
STAMP=$(date '+%Y-%m-%d %H:%M:%S')

if [ -f "$LOCKFILE" ]; then
  echo "[v12.2][$STAMP] 已有掛機執行中，退出" | tee -a "$LOGFILE"
  exit 1
fi
touch "$LOCKFILE"
START_TIME=$(date +%s)

# 輪次編號處理
if [ ! -f "$ROUND_FILE" ]; then
  echo "1" > "$ROUND_FILE"
fi
ROUND=$(cat "$ROUND_FILE")
NEXT_ROUND=$((ROUND + 1))
echo "$NEXT_ROUND" > "$ROUND_FILE"

echo "========== [v12.2] 第 $ROUND 輪 巡邏開始：$STAMP ==========" | tee -a "$LOGFILE"

MODULES=(
  "v01_auto_schema_guard.py"
  "v20_module_integrity_checker.py"
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
  "v16_eco_capital_allocator.py"
  "v17_eco_realistic_executor.py"
  "v18_eco_real_wallet_checker.py"
  "v19_eco_live_trading_switch.py"
  "v20_module_integrity_checker.py"
)

for MODULE in "${MODULES[@]}"; do
  echo "[v12.2] 執行中：$MODULE" | tee -a "$LOGFILE"
  python3 "/mnt/data/killcore/$MODULE" | tee -a "$LOGFILE"
done

# 抓取王者資訊
LATEST_KING=$(jq -r '.name' /mnt/data/killcore/king_pool.json 2>/dev/null)
LATEST_SYMBOL=$(jq -r '.symbol' /mnt/data/killcore/king_pool.json 2>/dev/null)
LATEST_SCORE=$(jq -r '.score' /mnt/data/killcore/king_pool.json 2>/dev/null)

echo "[v12.2] 本輪王者：$LATEST_KING / $LATEST_SYMBOL / score=$LATEST_SCORE" | tee -a "$LOGFILE"

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
echo "[v12.2] 執行時間：$ELAPSED 秒" | tee -a "$LOGFILE"
echo "========== [v12.2] 巡邏結束 ==========" | tee -a "$LOGFILE"

# 寫入 round_log.jsonl
echo "{\"round\": $ROUND, \"timestamp\": \"$STAMP\", \"name\": \"$LATEST_KING\", \"symbol\": \"$LATEST_SYMBOL\", \"score\": $LATEST_SCORE, \"elapsed\": $ELAPSED}" >> "$ROUND_LOG"

rm -f "$LOCKFILE"
