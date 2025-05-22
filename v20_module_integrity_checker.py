#!/usr/bin/env python3
# v20_module_integrity_checker.py - 模組結構防爆掃描器（無敵封頂版）

import json
import os

MODULE_DIR = "/mnt/data/killcore/modules"
SCHEMA_PATH = "/mnt/data/killcore/killcore_module_schema.json"
BAD_LIST_PATH = "/mnt/data/killcore/broken_modules.json"

def load_schema():
    try:
        with open(SCHEMA_PATH, "r") as f:
            return set(json.load(f).keys())
    except:
        print("[v20] 無法讀取模組結構標準（schema）")
        return set()

def validate_module(path, required_keys):
    try:
        with open(path, "r") as f:
            data = json.load(f)
        actual_keys = set(data.keys())
        missing = required_keys - actual_keys
        return len(missing) == 0, list(missing)
    except Exception as e:
        return False, [f"JSON 錯誤或無法讀取：{str(e)}"]

def scan_modules():
    required_keys = load_schema()
    broken_modules = []

    for file in os.listdir(MODULE_DIR):
        if file.endswith(".json"):
            full_path = os.path.join(MODULE_DIR, file)
            valid, issues = validate_module(full_path, required_keys)
            if not valid:
                broken_modules.append({
                    "file": file,
                    "issues": issues
                })
                try:
                    os.remove(full_path)
                    print(f"[v20] 已刪除損壞模組：{file}")
                except:
                    print(f"[v20] 無法刪除模組：{file}")

    with open(BAD_LIST_PATH, "w") as f:
        json.dump(broken_modules, f, indent=2)

    print(f"[v20] 結構檢查完成，損壞模組清單寫入：{BAD_LIST_PATH}")
    print(f"[v20] 共刪除 {len(broken_modules)} 筆模組")

def main():
    if not os.path.exists(MODULE_DIR):
        print("[v20] 模組資料夾不存在")
        return
    scan_modules()

if __name__ == "__main__":
    main()
