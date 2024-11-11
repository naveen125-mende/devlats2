#app/auth/auth_handler.py
import time
import jwt
import os 
from dotenv import load_dotenv

load_dotenv() 
JWT_SECRET = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv("ALGORITHM")

def token_response(token: str):
    return {"access_token": token}

def signJWT(user_email: str):
    payload = {"user_id": user_email,"expires": time.time() + 600 }
    print(payload)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    print("token created")
    return token_response(token)

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
