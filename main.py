import os
import requests
from dotenv import load_dotenv

load_dotenv()  # reads the .env file and loads values into environment

API_KEY = os.getenv("CRICAPI_KEY")
URL = "https://api.cricapi.com/v1/currentMatches"

INDIA_TEAMS = ["India", "India Women"]
IPL_KEYWORD = "Indian Premier League"

response = requests.get(URL, params={"apikey": API_KEY, "offset": 0})
data = response.json()

matches = data.get("data", [])

for match in matches:
    teams = match.get("teams", [])
    name = match.get("name", "")

    is_india_match = any(team in teams for team in INDIA_TEAMS)
    is_ipl_match = IPL_KEYWORD in name

    if is_india_match or is_ipl_match:
        print(match["name"])
        print("Status:", match["status"])
        print("---")