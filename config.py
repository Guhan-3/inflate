# Configuration settings 
import os
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
SECRET_KEY = os.getenv("SECRET_KEY","default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

RESET_TOKEN_EXPIRE_MINUTES = 15

SMTP_SERVER = "smtp.gmail.com" 
SMTP_PORT = 587  
SMTP_USER = "guhanmurugan1906@gmail.com"
SMTP_PASSWORD = "wqei awwe ofmn fuza"