import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv

load_dotenv()

# 获取数据库配置
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "shuihua")

# 构建 MySQL 连接字符串 (使用 pymysql 驱动)
# 格式: mysql+pymysql://user:password@host:port/dbname?charset=utf8mb4
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# 创建同步引擎
engine = create_engine(
    DATABASE_URL,
    echo=False, # 设置为 True 可打印 SQL 语句，方便调试
    pool_pre_ping=True, # 自动检测断开的连接
    pool_recycle=3600, # 连接回收时间
)

# 创建 Session 工厂
SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 声明模型基类
Base = declarative_base()

def init_db():
    """
    Ensure the database exists before creating tables.
    """
    from sqlalchemy import text
    try:
        # Try to connect to the specific database
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        # If database does not exist (MySQL error 1049)
        if "1049" in str(e) or "Unknown database" in str(e):
            print(f"Database '{DB_NAME}' does not exist. Creating it...")
            # Connect to MySQL server without database selected
            root_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?charset=utf8mb4"
            root_engine = create_engine(root_url)
            with root_engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print(f"Database '{DB_NAME}' created successfully.")
            # Dispose old engine to force reconnection
            engine.dispose()
        else:
            raise e

# 依赖注入函数
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


