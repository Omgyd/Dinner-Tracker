import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = os.urandom(12).hex()
    MONGO_URI = os.environ.get("MONGODB_URI")
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
