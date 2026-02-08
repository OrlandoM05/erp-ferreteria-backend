from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.modules.users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    oauth_token: str | None = Depends(oauth2_scheme),
    bearer: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    # 🔑 PRIORIDAD: Bearer manual > OAuth2
    token = None
    if bearer:
        token = bearer.credentials
    elif oauth_token:
        token = oauth_token

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.get(User, int(user_id))
    if not user or not user.is_active:
        raise credentials_exception

    return user


def require_role(*roles: str):
    def role_checker(user: User = Depends(get_current_user)):
        if not user.role or user.role.name not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role",
            )
        return user

    return role_checker
