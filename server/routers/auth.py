from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..security import verify_token
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..models import SysUser
from ..security import verify_sys_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["auth"])

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    username: str
    nick_name: str

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # 从 sys_user 表查询，排除已删除和已停用的用户
    user = db.query(SysUser).filter(
        SysUser.user_name == user_data.username,
        SysUser.del_flag == '0',
        SysUser.status == '0'
    ).first()
    
    if not user or not verify_sys_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name, "user_id": str(user.user_id)},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.user_id),
        "username": user.user_name,
        "nick_name": user.nick_name or user.user_name
    }



@router.get("/me")
def get_me(http_request: Request, db: Session = Depends(get_db)):
    auth_header = http_request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = verify_token(token)
            if payload and "user_id" in payload:
                user = db.query(SysUser).filter(SysUser.user_id == payload["user_id"]).first()
                if user:
                    return {
                        "user_id": str(user.user_id),
                        "username": user.user_name,
                        "nick_name": user.nick_name or user.user_name,
                        "position": user.position or "员工"
                    }
        except Exception:
            pass
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="未登录或Token已过期"
    )
