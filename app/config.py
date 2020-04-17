import os


SECRET_KEY = os.getenvb(b"SECRET_KEY")
SENTRY_DSN = os.getenv("SENTRY_DSN")

# Postgres
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_URI = (
     f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
)

# App-specific
ACCESS_TOKEN_EXPIRE_MINUTES = 60
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
FIRST_SUPERUSER_EMAIL = os.getenv("FIRST_SUPERUSER_EMAIL")
FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD")