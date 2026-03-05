# ============================================================================
# 文件: database.py
# 模块: server
# 职责: 数据库连接管理，提供 SQLAlchemy 引擎和 Session 工厂
#
# 依赖声明:
#   - 外部: os, sqlalchemy, dotenv
#
# 主要接口:
#   - engine: SQLAlchemy 引擎实例
#   - Base: ORM 模型基类 (declarative_base)
#   - get_db(): 依赖注入函数，返回数据库 Session
#   - init_db(): 初始化数据库（如果不存在）
#
# 环境变量:
#   - DB_USER: 数据库用户名 (默认: root)
#   - DB_PASSWORD: 数据库密码 (默认: 123456)
#   - DB_HOST: 数据库主机 (默认: localhost)
#   - DB_PORT: 数据库端口 (默认: 3306)
#   - DB_NAME: 数据库名称 (默认: shuihua)
#
# ============================================================================

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv

load_dotenv()

# 获取数据库配置
# Use explicit empty string as default for password if not set
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456") # Try 123456 as default fallback
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



