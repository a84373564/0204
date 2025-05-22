#!/bin/bash
# v12_killcore_runner.sh - Killcore 自動掛機巡邏流程（封頂防呆＋即時顯示）

LOCKFILE="/tmp/killcore_runner.lock"
LOGFILE="/mnt/data/killcore/killcore_runner.log"
STAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 防呆：已有執行中就退出
if [ -f "$LOCKFILE" ]; then
  echo "[v12][$STAMP] 已有掛機執行中，退出" | tee -a "$LOGFILE"
  exit 1
fi
touch "$LOCKFILE"
START_TIME=$(date +%s)

echo "========== [v12] 巡邏開始：$STAMP ==========" | tee -a "$LOGFILE"

# 執行模組清單
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

# 執行模組並即時顯示
for MODULE in "${MODULES[@]}"; do
  echo "[v12] 執行中：$MODULE" | tee -a "$LOGFILE"
  python3 "/mnt/data/killcore/$MODULE" | tee -a "$LOGFILE"
done

# 顯示本輪王者
LATEST_KING=$(jq -r '.name + " / " + .symbol + " / score=" + (.score|tostring)' /mnt/data/killcore/king_pool.json 2>/dev/null)
echo "[v12] 本輪王者：$LATEST_KING" | tee -a "$LOGFILE"

# 計算耗時
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
echo "[v12] 執行時間：$ELAPSED 秒" | tee -a "$LOGFILE"
echo "========== [v12] 巡邏結束 ==========" | tee -a "$LOGFILE"
rm -f "$LOCKFILE"
