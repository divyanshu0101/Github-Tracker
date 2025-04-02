from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import yaml

# Load Configuration
def load_config():
    with open("config.yml", 'r') as file:
        return yaml.safe_load(file)

config = load_config()
db_url = f"sqlite:///{config['database']['name']}"
engine = create_engine(db_url, echo=False)

Base = declarative_base()

class Repository(Base):
    __tablename__ = "repositories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    owner = Column(String)

class Branch(Base):
    __tablename__ = "branches"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    repository_id = Column(Integer, ForeignKey("repositories.id"))

class Commit(Base):
    __tablename__ = "commits"
    id = Column(Integer, primary_key=True)
    hash = Column(String, unique=True)
    branch_id = Column(Integer, ForeignKey("branches.id"))
    author = Column(String)
    date = Column(DateTime)
    message = Column(String)

class CodeChange(Base):
    __tablename__ = "code_changes"
    id = Column(Integer, primary_key=True)
    commit_id = Column(Integer, ForeignKey("commits.id"))
    added_lines = Column(Integer)
    removed_lines = Column(Integer)

# Initialize Database
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
