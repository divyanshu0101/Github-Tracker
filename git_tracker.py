import requests
import yaml
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Load Configuration
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

GITHUB_USERNAME = config["github"]["username"]
GITHUB_TOKEN = config["github"]["token"]
REPOSITORIES = config["github"]["repositories"]

DB_USER = config["database"]["user"]
DB_PASSWORD = config["database"]["password"]
DB_HOST = config["database"]["host"]
DB_PORT = config["database"]["port"]
DB_NAME = config["database"]["name"]

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Set up Database
Base = declarative_base()

class Repository(Base):
    __tablename__ = "repositories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    path = Column(String, nullable=False)

class Branch(Base):
    __tablename__ = "branches"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)

class Commit(Base):
    __tablename__ = "commits"
    id = Column(Integer, primary_key=True)
    hash = Column(String, nullable=False, unique=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False)
    author = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    message = Column(String, nullable=False)

class CodeChange(Base):
    __tablename__ = "code_changes"
    id = Column(Integer, primary_key=True)
    commit_id = Column(Integer, ForeignKey("commits.id"), nullable=False)
    added_lines = Column(Integer, nullable=False)
    removed_lines = Column(Integer, nullable=False)

# Connect to Database
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy import create_engine, inspect

engine = create_engine("postgresql://postgres:Root12345@localhost:5432/Git_tracker")

inspector = inspect(engine)
columns = inspector.get_columns("repositories")

print([column["name"] for column in columns])


# GitHub API Request Function
def github_api_request(url):
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
# Process Repositories
for repo_data in REPOSITORIES:
    repo_full_name = repo_data["name"]  # Extract repository name from dictionary
    owner, repo = repo_full_name.split("/")
    repo_path = repo_data.get("path", f"./repos/{repo_full_name.split('/')[1]}")  # Use path from YAML, fallback to default
    
    print(f"Processing repository: {repo}")

    # Store Repository
    repository = Repository(name=repo, owner=owner , path=repo_path)
    session.add(repository)

# Commit all changes at once (better performance)
    session.commit()

    # Get Branches
    branches_url = f"https://api.github.com/repos/{owner}/{repo}/branches"
    branches = github_api_request(branches_url)

    if not branches:
        continue

    for branch in branches:
        branch_name = branch["name"]
        print(f"  Processing branch: {branch_name}")

        # Store Branch
        branch_entry = Branch(name=branch_name, repository_id=repository.id)
        session.add(branch_entry)
        session.commit()

        # Get Commits
        commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits?sha={branch_name}"
        commits = github_api_request(commits_url)

        if not commits:
            continue

        previous_commit = None
        for commit in commits:
            commit_hash = commit["sha"]
            commit_author = commit["commit"]["author"]["name"]
            commit_date = datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
            commit_message = commit["commit"]["message"]

            # Store Commit
            commit_entry = Commit(hash=commit_hash, branch_id=branch_entry.id,
                                  author=commit_author, date=commit_date, message=commit_message)
            session.add(commit_entry)
            session.commit()

            # Get Code Changes (Using GitHub API instead of git diff)
            if previous_commit:
                diff_url = f"https://api.github.com/repos/{owner}/{repo}/compare/{previous_commit}...{commit_hash}"
                diff_data = github_api_request(diff_url)

                if diff_data and "files" in diff_data:
                    added = sum(file["additions"] for file in diff_data["files"])
                    removed = sum(file["deletions"] for file in diff_data["files"])

                    code_change = CodeChange(commit_id=commit_entry.id, added_lines=added, removed_lines=removed)
                    session.add(code_change)
                    session.commit()

            previous_commit = commit_hash

print("✅ Data retrieval and storage completed successfully!")
