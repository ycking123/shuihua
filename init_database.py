import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.getcwd())

def load_environment():
    """Load environment variables from multiple possible locations."""
    env_files = [
        Path(".env"),
        Path(".env.local"),
        Path("backend/.env"),
        Path("../.env"),
    ]
    
    env_loaded = False
    for env_file in env_files:
        if env_file.exists():
            # Use override=True to ensure the latest file takes precedence if multiple are loaded
            # Use encoding='utf-8' to handle Chinese characters in comments
            load_dotenv(dotenv_path=env_file, override=True, encoding='utf-8')
            print(f"✅ Loaded environment from {env_file}")
            env_loaded = True
            
    if not env_loaded:
        print("⚠️ No .env file found. Using system environment variables or defaults.")
        
    # Debug: Print loaded raw values (masked)
    print(f"DEBUG: DB_PORT raw: '{os.getenv('DB_PORT')}'")
    print(f"DEBUG: DB_USER raw: '{os.getenv('DB_USER')}'")
    
def init_database():
    print("=========================================")
    print("   Database Initialization Tool          ")
    print("=========================================")
    
    load_environment()
    
    # Configuration - Strip whitespace to handle potential trailing spaces
    db_user = (os.getenv("DB_USER") or "root").strip()
    db_password = (os.getenv("DB_PASSWORD") or "").strip()
    db_host = (os.getenv("DB_HOST") or "localhost").strip()
    db_port = (os.getenv("DB_PORT") or "3306").split('#')[0].strip() # Handle inline comments if dotenv didn't
    db_name = (os.getenv("DB_NAME") or "shuihua").strip()
    
    print(f"Target Database: {db_name}")
    print(f"Host: {db_host}:{db_port}")
    print(f"User: {db_user}")
    print(f"Password: {'******' if db_password else '(empty)'}")

    
    # 1. Connect to MySQL Server (no DB selected) to create DB
    root_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/?charset=utf8mb4"
    
    try:
        engine = create_engine(root_url)
        with engine.connect() as conn:
            print(f"🔄 Checking if database '{db_name}' exists...")
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print(f"✅ Database '{db_name}' ensured.")
    except Exception as e:
        print(f"❌ Failed to connect to MySQL server: {e}")
        print("Please ensure MySQL is running and credentials are correct.")
        return

    # 2. Connect to the specific database
    db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
    engine = create_engine(db_url)
    
    # 3. Read and execute init.sql
    init_sql_path = Path("init.sql")
    if not init_sql_path.exists():
        # Try finding it in current dir or parent
        init_sql_path = Path(__file__).parent / "init.sql"
        
    if not init_sql_path.exists():
        print("❌ init.sql not found!")
        return
        
    print(f"📖 Reading {init_sql_path}...")
    with open(init_sql_path, "r", encoding="utf-8") as f:
        sql_content = f.read()
        
    # Split statements (simple split by ';', ignoring comments/strings for now as init.sql is standard)
    # Better approach: use sqlalchemy execution of the whole script if possible, or split carefully.
    # Since init.sql might contain comments, we should be careful.
    # However, simple splitting by ';' usually works for DDL if no stored procs.
    
    statements = [s.strip() for s in sql_content.split(';') if s.strip()]
    
    print(f"🚀 Executing {len(statements)} statements...")
    
    success_count = 0
    with engine.connect() as conn:
        for stmt in statements:
            try:
                # Skip empty lines or comments-only
                if stmt.startswith("--") and "\n" not in stmt:
                    continue
                    
                conn.execute(text(stmt))
                conn.commit()
                success_count += 1
            except Exception as e:
                # Ignore "Table already exists" warnings if we want idempotent, 
                # but init.sql usually has CREATE TABLE without IF NOT EXISTS?
                # Let's check init.sql content. It uses CREATE TABLE.
                # If it fails, we report it.
                if "already exists" in str(e):
                    print(f"⚠️ Table already exists (skipped): {stmt[:50]}...")
                else:
                    print(f"❌ Error executing statement:\n{stmt[:100]}...\nError: {e}")
    
    print(f"✅ Initialization complete. Successfully executed {success_count} statements.")

if __name__ == "__main__":
    init_database()
