import requests
from datetime import datetime
from pathlib import Path

URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"
LOG_FILE = Path("history_log.txt")

PROXY = "http://qibirfry:3kaieqa2ut16@31.59.20.176:6754"
PROXIES = {"http": PROXY, "https": PROXY}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def big_small(num):
    return "BIG" if int(num) >= 5 else "SMALL"

def fetch_last_10():
    r = requests.get(URL, headers=HEADERS, proxies=PROXIES, timeout=20)
    r.raise_for_status()
    js = r.json()
    return js["data"]["list"][:10]  # latest 10 rounds

def load_logged_issues():
    if not LOG_FILE.exists():
        return set()
    issues = set()
    with LOG_FILE.open("r") as f:
        for line in f:
            parts = line.split("|")
            if len(parts) >= 2:
                issues.add(parts[1].strip())
    return issues

def append(entry):
    with LOG_FILE.open("a") as f:
        f.write(entry + "\n")

if __name__ == "__main__":
    LOG_FILE.touch(exist_ok=True)

    try:
        logged = load_logged_issues()
        rounds = fetch_last_10()

        new_count = 0

        # oldest → newest to keep order
        for item in reversed(rounds):
            issue = str(item["issueNumber"])
            number = str(item["number"])

            if issue in logged:
                continue

            entry = f"{now()} | {issue} | {number} | {big_small(number)}"
            append(entry)
            logged.add(issue)
            new_count += 1
            print("Logged:", entry)

        if new_count == 0:
            print("No new rounds this run")

    except Exception as e:
        print("Skipped run:", e)
