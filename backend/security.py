from passlib.context import CryptContext
import secrets

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

def encrypt_password(password):
    global pwd_context
    return pwd_context.encrypt(password)

def check_encrypted_password(password, hashed):
    global pwd_context
    try :
        return pwd_context.verify(password, hashed)
    except:
        return False
    
    return True

def activation_token():
    return secrets.token_urlsafe(32)

def login_token(username):
    return username + ':' + secrets.token_hex(32)
