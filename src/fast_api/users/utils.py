from passlib.context import CryptContext
import jwt
from fast_api.config import config
from datetime import datetime, timedelta

from uuid import uuid4
password_context = CryptContext(schemes=['bcrypt'])


def generate_password_hash(password : str) -> str:
    return password_context.hash(password)

def verify_password(password : str , password_hash : str) -> bool:
    return password_context.verify(password,password_hash)


def generate_access_token(user: dict, time_delta: timedelta , refresh = False) -> str:
    payload = {
        "user": user,
        "exp": datetime.now() + timedelta(seconds=time_delta) ,
        'jti': str(uuid4())  # Unique identifier for the token
    }

    payload["refresh"] = refresh

    # You can add expiration time here if needed
    encoded_jwt = jwt.encode(payload = payload, key=config.secret_key, algorithm=config.algorithm)
    return encoded_jwt

def decode_token(token: str) -> dict: 
    try:
        decoded_payload = jwt.decode(token, key=config.secret_key, algorithms=[config.algorithm])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    


from itsdangerous  import URLSafeTimedSerializer

serializer = URLSafeTimedSerializer(config.secret_key, salt="email-confirm-salt")


def generate_email_token(email: str) -> str:
    return serializer.dumps(email)      

def verify_email_token(token: str, ) -> str:
    try:
        email = serializer.loads(token)
        return email
    except Exception as e:
        raise Exception("Invalid or expired token")