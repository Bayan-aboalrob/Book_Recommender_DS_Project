from dotenv import load_dotenv
import os
import redis

load_dotenv()  # loads the environment variables from the .env file.


class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"

    # By configuring these settings, your Flask application will use Redis as the session storage backend, allowing you to store and manage user sessions securely using Redis.
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
