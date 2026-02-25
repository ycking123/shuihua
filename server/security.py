# ============================================================================
# 文件: security.py
# 模块: server
# 职责: 安全认证相关工具，密码加密，JWT 令牌管理
#
# 依赖声明:
#   - 外部: datetime, typing, jose, passlib, os
#
# 主要接口:
#   - verify_password(plain_password, hashed_password): 验证密码
#   - get_password_hash(password): 生成密码哈希
#   - create_access_token(data, expires_delta): 创建 JWT 令牌
#   - verify_token(token): 验证 JWT 令牌
#
# 环境变量:
#   - SECRET_KEY: JWT 签名密钥
#
# ============================================================================

from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
import os

# 配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-should-be-in-env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days for convenience

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None


