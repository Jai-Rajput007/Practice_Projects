# app/security.py
import os
import hashlib
from passlib.context import CryptContext

# --- Environment Variables ---
SERVER_SECRET_KEY = os.getenv("SERVER_SECRET_KEY")
PUBLIC_INTERMEDIATE_KEY = int(os.getenv("PUBLIC_INTERMEDIATE_KEY", 101))

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# --- Cyclic Proof Hash Generation ---
def create_cyclic_proof_hash(round_number: int, user_secret_key: str) -> str:
    # ... (this function is correct and remains unchanged) ...
    value1 = round_number % (PUBLIC_INTERMEDIATE_KEY - 3)
    value2 = round_number % (PUBLIC_INTERMEDIATE_KEY - 2)
    value3 = round_number % (PUBLIC_INTERMEDIATE_KEY - 1)
    
    combined_string = f"{user_secret_key}-{value1}-{value2}-{value3}-{SERVER_SECRET_KEY}"
    
    hasher = hashlib.sha256()
    hasher.update(combined_string.encode('utf-8'))
    
    return hasher.hexdigest()

# --- Generate a random secret key for new users ---
def generate_user_secret():
    return hashlib.sha256(os.urandom(60)).hexdigest()