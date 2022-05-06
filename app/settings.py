from dotenv import dotenv_values

env = dotenv_values(".env")

SECRET_KEY = env["SECRET_KEY"]
ALGORITHM = env["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = env["ACCESS_TOKEN_EXPIRE_MINUTES"]

ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]
