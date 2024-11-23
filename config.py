# Configuration settings 
import os
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://inflate:inflate%40123@user.y39b2.mongodb.net/")
SECRET_KEY = os.getenv("SECRET_KEY","default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

RESET_TOKEN_EXPIRE_MINUTES = 15

SMTP_SERVER = "smtp.gmail.com" 
SMTP_PORT = 587  
SMTP_USER = "smguhan1926@gmail.com"
SMTP_PASSWORD = "wjxf rxjg tahc ojnq"