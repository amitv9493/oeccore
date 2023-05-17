import environ

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env()
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", False)
