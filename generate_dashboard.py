import os
import requests
from datetime import datetime
import json

GITHUB_USER = "somsoo"
TOKEN = os.environ.get("GITHUB_TOKEN")

headers = {"Accept": "application/vnd.github.v3+json"}
if TOKEN:
    headers["Authorization"] = f"token {TOKEN}"

repos_url = f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100"
response = requests.get(repos_url, headers=headers)

if response.status_code != 200:
    print(f"Failed to fetch repos: {response.status_code}")
    exit(1)

repos = response.json()
factory_sites = []

def parse_bom_json(text):
    if text.startswith('\ufeff'):
        text = text[1:]
    return json.loads(text)

for repo in repos:
    repo_name = repo["name"]
    raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{repo_name}/main/.factory.json"
    meta_resp = requests.get(raw_url, headers=headers)
    
    if meta_resp.status_code == 200:
        try:
            meta = parse_bom_json(meta_resp.text)
            meta["repo"] = repo_name
            if not meta.get("domain") and meta.get("type") != "threads":
                meta["domain"] = f"{repo_name}.enjoy-onepage.com"
            
            if meta.get("domain"):
                meta["url"] = f"https://{meta['domain']}"
            
            if meta["type"] == "cpa":
                camp_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{repo_name}/main/campaigns.json"
                camp_resp = requests.get(camp_url, headers=headers)
                if camp_resp.status_code == 200:
                    meta["campaign_count"] = len(parse_bom_json(camp_resp.text))
                else:
                    meta["campaign_count"] = 0
            
            elif meta["type"] == "threads":
                db_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{repo_name}/main/database.json"
                db_resp = requests.get(db_url, headers=headers)
                if db_resp.status_code == 200:
                    db_data = parse_bom_json(db_resp.text)
                    accounts = db_data.get("accounts", [])
                    meta["accounts"] = [acc.get("username", "Unknown") for acc in accounts]
                else:
                    meta["accounts"] = []
            
            factory_sites.append(meta)
        except Exception as e:
            print(f"Error parsing .factory.json in {repo_name}: {e}")

readme_content = f"# 🏭 Factory Control Dashboard\n\n"
readme_content += f"> Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC)\n\n"

cpa_sites = [s for s in factory_sites if s.get("type") == "cpa"]
threads_bots = [s for s in factory_sites if s.get("type") == "threads"]
onepage_sites = [s for s in factory_sites if s.get("type") == "onepage"]

readme_content += f"## 📈 CPA Blogs ({len(cpa_sites)} Sites)\n\n"
readme_content += "| Repository | Domain | Active Campaigns |\n"
readme_content += "|---|---|---|\n"
for site in cpa_sites:
    readme_content += f"| [{site['repo']}](https://github.com/{GITHUB_USER}/{site['repo']}) | [{site['domain']}]({site['url']}) | {site.get('campaign_count', 0)} |\n"

readme_content += f"\n## 📱 Threads Bots ({len(threads_bots)} Repositories)\n\n"
if not threads_bots:
    readme_content += "*No bots registered yet.*\n\n"
else:
    for bot in threads_bots:
        readme_content += f"### [{bot['repo']}](https://github.com/{GITHUB_USER}/{bot['repo']})\n"
        accounts = bot.get("accounts", [])
        readme_content += f"- **Operating Accounts ({len(accounts)}):**\n"
        for acc in accounts:
            readme_content += f"  - `@{acc}`\n"
        readme_content += "\n"

readme_content += f"\n## 🚀 Onepage Landings ({len(onepage_sites)} Sites)\n\n"
readme_content += "*No onepage sites registered yet.*\n\n" if not onepage_sites else ""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("Dashboard README.md generated successfully.")
