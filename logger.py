import requests
from datetime import datetime
from pathlib import Path

URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"
LOG_FILE = Path("history_log.txt")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (WinGoLogger/1.0)",
    "Accept": "application/json"
}

def now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def big_small(num):
    return "BIG" if int(num) >= 5 else "SMALL"

def fetch_latest():
    r = requests.get(URL, headers=HEADERS, timeout=10)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}")

    try:
        js = r.json()
    except Exception:
        raise RuntimeError("Non-JSON response")

    data = js.get("data", {}).get("list", [])
    if not data:
        raise RuntimeError("Empty data list")

    item = data[0]
    return str(item["issueNumber"]), str(item["number"])

def ensure_file():
    if not LOG_FILE.exists():
        LOG_FILE.write_text("")  # create empty file

def already_logged(issue):
    if not LOG_FILE.exists():
        return False
    with LOG_FILE.open("r") as f:
        for line in f:
            if f"| {issue} |" in line:
                return True
    return False

def log(issue, number):
    entry = f"{now()} | {issue} | {number} | {big_small(number)}"
    with LOG_FILE.open("a") as f:
        f.write(entry + "\n")
    print("Logged:", entry)

if __name__ == "__main__":
    ensure_file()

    try:
        issue, number = fetch_latest()
        if already_logged(issue):
            print("Already logged:", issue)
        else:
            log(issue, number)
    except Exception as e:
        # IMPORTANT: file still exists so GitHub can commit
        print("Skipped this run:", e)
