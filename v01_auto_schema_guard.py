#!/usr/bin/env python3
# v01_auto_schema_guard.py
import os
import json
import glob

MODULE_DIR = "/mnt/data/killcore/modules"
SCHEMA_PATH = "/mnt/data/killcore/killcore_module_schema.json"
LOG_PATH = "/mnt/data/killcore/v01_guard_log.txt"

def load_schema():
    with open(SCHEMA_PATH, "r") as f:
        return json.load(f)

def load_module(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return None

def save_module(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def validate_and_repair_module(module, schema):
    repaired = False
    for key in schema:
        if key not in module:
            module[key] = schema[key]
            repaired = True
    return module, repaired

def main():
    schema = load_schema()
    module_files = glob.glob(f"{MODULE_DIR}/*.json")
    repaired_count, deleted_count = 0, 0

    with open(LOG_PATH, "w") as log:
        for path in module_files:
            mod = load_module(path)
            if not mod:
                os.remove(path)
                deleted_count += 1
                log.write(f"[刪除] 無法讀取：{os.path.basename(path)}\n")
                continue

            mod, repaired = validate_and_repair_module(mod, schema)
            if repaired:
                save_module(path, mod)
                repaired_count += 1
                log.write(f"[修復] 欄位補全：{os.path.basename(path)}\n")

    print(f"[v01] 修復完成：{repaired_count} 筆，刪除錯誤模組：{deleted_count} 筆")

if __name__ == "__main__":
    main()
