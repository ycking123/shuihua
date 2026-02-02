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

# 依赖注入函数
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

