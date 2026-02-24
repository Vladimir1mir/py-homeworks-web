import os

POSTGRES_DB=os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST=os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_USER=os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PORT=os.getenv("POSTGRES_PORT", "5432")

PG_DSN = (
    f"postgresql+asyncpg://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

TOKEN_TTL_SEC = 60 * 60 * 48