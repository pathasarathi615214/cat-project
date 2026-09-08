import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

DB_URL = os.getenv("DB_URL", f"sqlite:///{BASE_DIR / 'ci_bottleneck.db'}")
