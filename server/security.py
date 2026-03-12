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
import bcrypt
import os

# 配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-should-be-in-env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days for convenience

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """验证 pbkdf2_sha256 格式的密码"""
    return pwd_context.verify(plain_password, hashed_password)

def verify_sys_password(plain_password: str, stored_password: str) -> bool:
    """验证 sys_user 表的密码（支持 bcrypt 和 pbkdf2_sha256 哈希）"""
    if not stored_password:
        return False
    # bcrypt 哈希格式：$2a$, $2b$, $2y$
    if stored_password.startswith('$2'):
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                stored_password.encode('utf-8')
            )
        except Exception:
            return False
    # pbkdf2_sha256 等其他 passlib 支持的哈希格式
    if stored_password.startswith('$'):
        try:
            return pwd_context.verify(plain_password, stored_password)
        except Exception:
            return False
    # 非哈希格式一律拒绝，不允许明文密码
    return False

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



