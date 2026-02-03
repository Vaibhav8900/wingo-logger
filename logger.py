import requests
from datetime import datetime

URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"
LOG_FILE = "history_log.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WinGoLogger/1.0)",
    "Accept": "application/json"
}

def now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def big_small(num):
    return "BIG" if int(num) >= 5 else "SMALL"

def fetch_latest():
    r = requests.get(URL, headers=HEADERS, timeout=10)

    # ❗ API sometimes returns HTML / empty
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

def already_logged(issue):
    try:
        with open(LOG_FILE, "r") as f:
            return issue in f.read()
    except FileNotFoundError:
        return False

def log(issue, number):
    entry = f"{now()} | {issue} | {number} | {big_small(number)}"
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")
    print(entry)

if __name__ == "__main__":
    try:
        issue, number = fetch_latest()
        if not already_logged(issue):
            log(issue, number)
        else:
            print("Already logged:", issue)
    except Exception as e:
        # IMPORTANT: do NOT crash the action
        print("Skipped this run:", e)
