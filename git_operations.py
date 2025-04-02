import os
import git
import yaml
from github_fetcher import fetch_repositories
from logger import setup_logger

# Load Configuration
def load_config():
    with open("config.yml", 'r') as file:
        return yaml.safe_load(file)

config = load_config()
logger = setup_logger()

def clone_or_update_repositories():
    repositories = fetch_repositories()
    base_path = os.path.join(os.getcwd(), "data")

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    for repo_name in repositories:
        repo_path = os.path.join(base_path, repo_name)

        if not os.path.exists(repo_path):
            try:
                logger.info(f"Cloning repository {repo_name}...")
                git.Repo.clone_from(f'https://github.com/{config["github_username"]}/{repo_name}.git', repo_path)
            except Exception as e:
                logger.error(f"Failed to clone {repo_name}: {e}")
        else:
            try:
                logger.info(f"Updating repository {repo_name}...")
                repo = git.Repo(repo_path)
                repo.remotes.origin.pull()
            except Exception as e:
                logger.error(f"Failed to update {repo_name}: {e}")

if __name__ == "__main__":
    clone_or_update_repositories()
