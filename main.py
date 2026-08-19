import requests

API_KEY = "ebd4191c-960d-4cc5-a348-fb278f959ce3"
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