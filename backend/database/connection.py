import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = quote_plus(os.getenv("DATABASE_PASSWORD"))
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = (
    f"postgresql://{DATABASE_USER}:"
    f"{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:"
    f"{DATABASE_PORT}/"
    f"{DATABASE_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True
)