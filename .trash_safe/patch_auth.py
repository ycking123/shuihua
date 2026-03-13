with open('server/routers/auth.py', 'r') as f:
    text = f.read()

text = text.replace('from fastapi import APIRouter, Depends, HTTPException, status', 'from fastapi import APIRouter, Depends, HTTPException, status, Request\nfrom ..security import verify_token')

new_route = '''
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
'''
with open('server/routers/auth.py', 'w') as f:
    f.write(text + new_route)

