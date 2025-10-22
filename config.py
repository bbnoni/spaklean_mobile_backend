import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://spaklean_db_mobile_user:BkBXGsabaLp23dnKxohjEH2N9WXFUuCZ@dpg-d3selkk9c44c73com7eg-a.oregon-postgres.render.com/spaklean_db_mobile"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "spaklean_secret_key"
