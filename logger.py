import logging
import os
import yaml

def load_config():
    with open("config.yml", 'r') as file:
        return yaml.safe_load(file)

config = load_config()

def setup_logger():
    log_file = config["logging"]["file"]
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger()

logger = setup_logger()
