import requests
from datetime import datetime
from pathlib import Path

URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"
LOG_FILE = Path("history_log.txt")

PROXY = "http://qibirfry:3kaieqa2ut16@6754:31.59.20.176"  # 👈 PUT YOUR PROXY HERE

PROXIES = {
    "http": PROXY,
    "https": PROXY
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def big_small(num):
    return "BIG" if int(num) >= 5 else "SMALL"

def fetch_latest():
    r = requests.get(
        URL,
        headers=HEADERS,
        proxies=PROXIES,
        timeout=15
    )

    js = r.json()
    item = js["data"]["list"][0]
    return str(item["issueNumber"]), str(item["number"])

def already_logged(issue):
    if not LOG_FILE.exists():
        return False
    return issue in LOG_FILE.read_text()

def log(issue, number):
    entry = f"{now()} | {issue} | {number} | {big_small(number)}"
    LOG_FILE.write_text(LOG_FILE.read_text() + entry + "\n" if LOG_FILE.exists() else entry + "\n")
    print("Logged:", entry)

if __name__ == "__main__":
    try:
        issue, number = fetch_latest()
        if not already_logged(issue):
            log(issue, number)
        else:
            print("Already logged")
    except Exception as e:
        print("Skipped:", e)