import requests
from datetime import datetime

URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"
LOG_FILE = "history_log.txt"

def now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def big_small(num):
    return "BIG" if int(num) >= 5 else "SMALL"

def fetch_latest():
    r = requests.get(URL, timeout=10)
    data = r.json()["data"]["list"][0]
    return data["issueNumber"], str(data["number"])

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
    issue, number = fetch_latest()
    if not already_logged(issue):
        log(issue, number)
