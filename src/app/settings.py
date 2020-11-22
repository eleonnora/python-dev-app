# Load ENV variables

import os
from dotenv import load_dotenv
load_dotenv()

SECRET = os.getenv("SECRET")
ACCESS_KEY = os.getenv("ACCESS_KEY")
REGION_NAME = os.getenv("REGION_NAME")
