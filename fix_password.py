import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from passlib.context import CryptContext

# Find env file relative to this script
script_dir = Path(__file__).parent
env_path = script_dir / "backend" / ".env"
print(f"Loading env from: {env_path}")
load_dotenv(env_path)

db_user = (os.getenv("DB_USER") or "root").strip()
db_password = (os.getenv("DB_PASSWORD") or "").strip()
db_host = (os.getenv("DB_HOST") or "localhost").strip()
db_port = (os.getenv("DB_PORT") or "3306").split('#')[0].strip()
db_name = (os.getenv("DB_NAME") or "shuihua").strip()

db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        # Find users with plain text passwords (heuristically, short or missing $)
        # Actually, specifically fixing 'yc' as seen in diagnosis
        print("Checking user 'yc'...")
        result = conn.execute(text("SELECT id, password_hash FROM shjl_users WHERE username = 'yc'"))
        user = result.fetchone()
        
        if user:
            uid, current_hash = user
            print(f"User 'yc' found. Current hash: {current_hash}")
            
            if not current_hash.startswith("$"):
                print("Detected plain text or invalid hash. Updating to hashed '123456'...")
                new_hash = get_password_hash("123456")
                conn.execute(
                    text("UPDATE shjl_users SET password_hash = :ph WHERE id = :uid"),
                    {"ph": new_hash, "uid": uid}
                )
                conn.commit()
                print("✅ Password updated successfully.")
            else:
                print("Password appears to be hashed already.")
        else:
            print("User 'yc' not found.")
            
except Exception as e:
    print(f"Error: {e}")
