import sys
import os
from sqlalchemy import create_engine, inspect, text
from dotenv import load_dotenv

# Add the current directory to sys.path to ensure we can import server modules if needed
sys.path.append(os.getcwd())

def check_db_connection():
    print("=========================================")
    print("   Database Connection Diagnostic Tool   ")
    print("=========================================")
    
    # Load env
    load_dotenv() # Load .env file by default
    
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "shuihua")
    
    print(f"Configuration:")
    print(f"  Host: {db_host}")
    print(f"  Port: {db_port}")
    print(f"  User: {db_user}")
    print(f"  Database: {db_name}")
    print(f"  Password: {'******' if db_password else '(empty)'}")
    
    # Construct URL
    # Try different drivers if one fails
    urls = [
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4",
        f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
    ]
    
    success = False
    
    for url in urls:
        driver = url.split(":")[0]
        print(f"\nAttempting connection using {driver}...")
        try:
            engine = create_engine(url)
            with engine.connect() as conn:
                print("  Connection Successful!")
                result = conn.execute(text("SELECT 1")).fetchone()
                print(f"  Test Query (SELECT 1): {result[0]}")
                
                print("  Checking tables...")
                inspector = inspect(engine)
                tables = inspector.get_table_names()
                print(f"  Found {len(tables)} tables: {', '.join(tables)}")
                
                required_tables = ["shjl_users", "shjl_todos"]
                missing = [t for t in required_tables if t not in tables]
                
                if missing:
                    print(f"  [ERROR] Missing critical tables: {', '.join(missing)}")
                    print("  Try restarting the server to trigger auto-creation.")
                else:
                    print("  [OK] Critical tables found.")
                    
            success = True
            break
        except ImportError:
            print(f"  [SKIP] Driver not installed for {driver}")
        except Exception as e:
            print(f"  [FAIL] Connection failed: {e}")
            
    if not success:
        print("\n[FATAL] Could not connect to database with any driver.")
        print("Please check your database server status and credentials.")
    else:
        print("\n[SUCCESS] Database check passed.")

if __name__ == "__main__":
    check_db_connection()

