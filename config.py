import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BCRA_API_TOKEN = os.getenv("BCRA_API_TOKEN")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definido en el entorno")

if not BCRA_API_TOKEN:
    raise ValueError("BCRA_API_TOKEN no está definido en el entorno")