#!/usr/bin/env python3
# v05_strategy_generator.py - Killcore 無敵策略模組產生器（A～J 十類型、王者復活、補血）

import os, json, random, time

SCHEMA_PATH = "/mnt/data/killcore/killcore_module_schema.json"
SYMBOLS_PATH = "/mnt/data/killcore/symbol_filtered.json"
MEMORY_PATH = "/mnt/data/killcore/memory_bank.json"
KING_POOL_PATH = "/mnt/data/killcore/king_pool.json"
MODULES_DIR = "/mnt/data/killcore/modules"

TOTAL_MODULES = 500
STRATEGY_TYPES = list("ABCDEFGHIJ")  # A～J 共十類
WDRR = {2: 0.2, 3: 0.4, 4: 0.6, 5: 0.8}

os.makedirs(MODULES_DIR, exist_ok=True)

def load_json(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def avoid_dead(memory, strategy, params):
    for dead in memory:
        if dead.get("strategy") == strategy and dead.get("params") == params:
            return False
    return True

def generate_strategy(strategy_type):
    # 每種策略對應不同參數邏輯
    base_params = {
        "A": {"ma_period": random.randint(5, 20)},
        "B": {"rsi_threshold": random.randint(30, 70)},
        "C": {"breakout_window": random.randint(10, 50)},
        "D": {"volatility_window": random.randint(5, 30)},
        "E": {"momentum_strength": round(random.uniform(0.5, 2.0), 2)},
        "F": {"mean_revert_range": random.randint(2, 15)},
        "G": {"macd_fast": 12, "macd_slow": 26},
        "H": {"bb_window": random.randint(10, 30)},
        "I": {"atr_factor": round(random.uniform(1.0, 3.0), 2)},
        "J": {"supertrend_period": random.randint(5, 20)}
    }
    return strategy_type, base_params.get(strategy_type, {})

def generate_module(name, symbol, strategy, params, from_retry=False):
    mod = {
        "name": name,
        "symbol": symbol,
        "strategy": strategy,
        "params": params,
        "from_retry": from_retry,
        "score": None,
        "history": [],
        "log": [],
        "created_at": int(time.time())
    }
    schema = load_json(SCHEMA_PATH, {})
    for key in schema:
        if key not in mod:
            mod[key] = schema[key]
    return mod

def main():
    memory = load_json(MEMORY_PATH, [])
    symbols = load_json(SYMBOLS_PATH, [])
    king_pool = load_json(KING_POOL_PATH, {})
    modules = []
    counter = {k: 1 for k in STRATEGY_TYPES}

    # 處理王者復活（WDRR）
    if king_pool:
        king = king_pool
        strategy = king.get("strategy")
        params = king.get("params")
        symbol = king.get("symbol")
        strategy_type = strategy[0] if strategy else "A"
        count = king.get("king_count", 1)
        w = WDRR.get(count, 0)
        if random.random() < w:
            name = f"{strategy_type}-{counter[strategy_type]}"
            counter[strategy_type] += 1
            modules.append(generate_module(name, symbol, strategy, params, from_retry=True))

    # 補足模組數量（補血機制）
    while len(modules) < TOTAL_MODULES:
        stype = random.choice(STRATEGY_TYPES)
        strategy, params = generate_strategy(stype)
        symbol = random.choice(symbols) if symbols else "BTCUSDT"
        if avoid_dead(memory, strategy, params):
            name = f"{stype}-{counter[stype]}"
            counter[stype] += 1
            mod = generate_module(name, symbol, strategy, params, from_retry=False)
            modules.append(mod)

    # 寫入 modules 目錄
    for mod in modules:
        filename = f"{mod['name']}.json"
        save_json(os.path.join(MODULES_DIR, filename), mod)

    print(f"[v05] 產生模組完成：{len(modules)} 支")

if __name__ == "__main__":
    main()
