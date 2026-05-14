import json
import os
import subprocess

# 配置
UPDATE_JSON = "update.json"
GITHUB_USER = "alanpicarrot"
GITHUB_REPO = "echomrhoney_update"

def update_json_file():
    # 讀取現有的或建立新的
    if os.path.exists(UPDATE_JSON):
        with open(UPDATE_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {
            "versionCode": 0,
            "versionName": "0.0.0",
            "url": "",
            "releaseNotes": "",
            "forceUpdate": False
        }
    
    # 手動輸入版本資訊
    print("--- 手動輸入版本資訊 ---")
    try:
        version_code = int(input(f"請輸入新的 versionCode (目前: {data['versionCode']}): "))
        version_name = input(f"請輸入新的 versionName (目前: {data['versionName']}): ")
    except ValueError:
        print("錯誤: versionCode 必須是數字")
        return

    data["versionCode"] = version_code
    data["versionName"] = version_name
    
    # 假設 Release URL 格式如下
    data["url"] = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/releases/download/{version_name}/app-release.apk"
    
    print(f"\n目前設定版本: {version_name} ({version_code})")
    notes = input("請輸入更新日誌 (直接按 Enter 跳過): ")
    if notes:
        data["releaseNotes"] = notes
        
    force = input("是否強制更新? (y/N): ").lower() == 'y'
    data["forceUpdate"] = force

    with open(UPDATE_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 已更新 {UPDATE_JSON}")

def git_push():
    confirm = input("\n是否提交並推送到 GitHub? (y/N): ").lower()
    if confirm == 'y':
        try:
            subprocess.run(["git", "add", UPDATE_JSON], check=True)
            subprocess.run(["git", "commit", "-m", f"chore: update version to {UPDATE_JSON}"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("🚀 已成功推送至 GitHub")
        except subprocess.CalledProcessError as e:
            print(f"❌ Git 操作失敗: {e}")

if __name__ == "__main__":
    try:
        update_json_file()
        git_push()
    except Exception as e:
        print(f"❌ 錯誤: {e}")
