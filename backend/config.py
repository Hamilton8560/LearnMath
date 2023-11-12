import os

LOGFILE_LOCATION = os.getenv("LOG_LOCATION", "./all.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

CONTEXT_PATH = os.getenv("CONTEXT_PATH", "/api")
SECRET_KEY = os.getenv("SECRET_KEY", "")
