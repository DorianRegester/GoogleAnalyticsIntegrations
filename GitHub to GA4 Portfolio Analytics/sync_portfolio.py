import os
import requests
import json

# Securely pull from GitHub Environment
PAT = os.getenv('PAT_TOKEN')
GA4_ID = os.getenv('GA4_MEASUREMENT_ID')
GA4_SECRET = os.getenv('GA4_API_SECRET')

def send_to_ga4(event_name, params):
    url = f"https://www.google-analytics.com/mp/collect?measurement_id={GA4_ID}&api_secret={GA4_SECRET}"
    payload = {
        "client_id": "portfolio_engine",
        "non_personalized_ads": True,
        "events": [{"name": event_name, "params": params}]
    }
    requests.post(url, json=payload)

def get_all_repos():
    # per_page=100 ensures we catch all 75+ repos in one call
    url = "https://api.github.com/user/repos?per_page=100&type=owner"
    headers = {"Authorization": f"token {PAT}"}
    return requests.get(url, headers=headers).json()

def run_sync():
    repos = get_all_repos()
    headers = {"Authorization": f"token {PAT}"}

    for repo in repos:
        name = repo['full_name']
        print(f"Syncing: {name}")

        # 1. Fetch Traffic (Views)
        views = requests.get(f"https://api.github.com/repos/{name}/traffic/views", headers=headers).json()
        daily_v = views.get('views', [])[-1].get('count', 0) if views.get('views') else 0

        # 2. Fetch Clones (Downloads)
        clones = requests.get(f"https://api.github.com/repos/{name}/traffic/clones", headers=headers).json()
        daily_c = clones.get('clones', [])[-1].get('count', 0) if clones.get('clones') else 0

        # 3. Fetch Popular Paths (Folders/Files)
        paths = requests.get(f"https://api.github.com/repos/{name}/traffic/popular/paths", headers=headers).json()

        # Send Main Repo Stats
        send_to_ga4("github_repo_daily", {
            "repo_name": name,
            "stars": repo.get('stargazers_count', 0),
            "forks": repo.get('forks_count', 0),
            "daily_views": daily_v,
            "daily_clones": daily_c
        })

        # Send Folder/File Specific Views (Top 5)
        for p in paths[:5]:
            send_to_ga4("github_file_view", {
                "repo_name": name,
                "file_path": p['path'],
                "file_views": p['count']
            })

if __name__ == "__main__":
    run_sync()
