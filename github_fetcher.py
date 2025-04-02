import requests
import yaml

# Load Configuration
def load_config():
    with open("config.yml", 'r') as file:
        return yaml.safe_load(file)

config = load_config()

def fetch_repositories():
    url = f"https://api.github.com/users/{config['github_username']}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        repos = [repo["name"] for repo in response.json()]
        return repos
    else:
        print("❌ Error fetching repositories:", response.json())
        return []

if __name__ == "__main__":
    print(fetch_repositories())
