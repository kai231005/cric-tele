import os
import requests
from dotenv import load_dotenv

load_dotenv()

CRIC_API_KEY = os.getenv("CRICAPI_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

CRIC_URL = "https://api.cricapi.com/v1/currentMatches"
INDIA_TEAMS = ["India", "India Women"]
IPL_KEYWORD = "Indian Premier League"


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})


def fetch_matches():
    response = requests.get(CRIC_URL, params={"apikey": CRIC_API_KEY, "offset": 0})
    data = response.json()
    return data.get("data", [])


def filter_relevant(matches):
    relevant = []
    for match in matches:
        teams = match.get("teams", [])
        name = match.get("name", "")

        is_india_match = any(team in teams for team in INDIA_TEAMS)
        is_ipl_match = IPL_KEYWORD in name

        if is_india_match or is_ipl_match:
            relevant.append(match)

    return relevant


def format_match(match):
    result_type = "FINISHED" if match.get("matchEnded") else "LIVE/UPCOMING"
    return f"[{result_type}] {match['name']}\nStatus: {match['status']}"


def main():
    matches = fetch_matches()
    relevant = filter_relevant(matches)

    if relevant:
        messages = [format_match(m) for m in relevant]
    else:
        # fallback: no India/IPL match right now, send top 5 matches happening elsewhere
        fallback = matches[:5]
        messages = ["No India/IPL matches right now. Here's what's happening elsewhere:"]
        messages += [format_match(m) for m in fallback]

    full_text = "\n\n".join(messages)
    send_telegram_message(full_text)
    print("Message sent to Telegram:")
    print(full_text)


if __name__ == "__main__":
    main()