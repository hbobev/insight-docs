import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings
from schemas.authentication_schema import TokenPayload, UserInDB, UserResponse
from shared.exceptions.base import AuthenticationError

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory token blacklist (in production, use Redis or similar)
revoked_tokens: set[str] = set()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password to compare against

    Returns:
        True if the password matches the hash, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time

    Returns:
        JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    token_id = (
        f"access-{data.get('sub', 'unknown')}-{datetime.now(timezone.utc).timestamp()}"
    )
    to_encode.update(
        {
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "access",
            "jti": token_id,
        }
    )

    token = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    logger.info(f"Access token created for user {data.get('sub', 'unknown')}")
    return token


def decode_token(token: str) -> TokenPayload:
    """
    Decode a JWT token.

    Args:
        token: JWT token to decode

    Returns:
        Decoded token payload

    Raises:
        AuthenticationError: If the token is invalid or revoked
    """
    try:
        if is_token_revoked(token):
            raise AuthenticationError("Token has been revoked")

        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return TokenPayload(**payload)
    except JWTError as e:
        logger.error(f"Error decoding token: {e}")
        raise AuthenticationError("Invalid token")


async def authenticate_user(username: str, password: str) -> dict[str, Any]:
    """
    Authenticate a user.

    Args:
        username: Username
        password: Password

    Returns:
        User data if authentication is successful

    Raises:
        AuthenticationError: If authentication fails
    """
    if username != settings.ADMIN_USERNAME:
        logger.warning(f"Authentication failed: User {username} not found")
        raise AuthenticationError("Invalid username or password")

    # Use configured admin password
    hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
    if not verify_password(password, hashed_password):
        logger.warning(f"Authentication failed: Invalid password for user {username}")
        raise AuthenticationError("Invalid username or password")

    user_data = UserInDB(
        id="admin-user-id",
        username=username,
        email=settings.ADMIN_EMAIL,
        role="admin",
        is_active=True,
        hashed_password=hashed_password,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    user_response = UserResponse(
        id=user_data.id,
        username=user_data.username,
        email=user_data.email,
        role=user_data.role,
        is_active=user_data.is_active,
        created_at=user_data.created_at,
        updated_at=user_data.updated_at,
    )

    logger.info(f"User {username} successfully authenticated")
    return user_response.model_dump()


def create_refresh_token(user_id: str) -> str:
    """
    Create a refresh token for a user.

    Args:
        user_id: User ID

    Returns:
        Refresh token
    """
    expires = datetime.now(timezone.utc) + timedelta(days=7)
    token_id = f"refresh-{user_id}-{datetime.now(timezone.utc).timestamp()}"

    to_encode = {
        "sub": user_id,
        "exp": expires,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
        "jti": token_id,
    }

    token = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    logger.info(f"Refresh token created for user {user_id}")
    return token


def revoke_token(token: str) -> None:
    """
    Revoke a token by adding it to the blacklist.

    Args:
        token: Token to revoke
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_id = payload.get("jti")
        if token_id:
            revoked_tokens.add(token_id)
            logger.info(f"Token {token_id[:8]}... has been revoked")
    except JWTError:
        logger.error("Failed to decode token for revocation")
        raise AuthenticationError("Invalid token")


def is_token_revoked(token: str) -> bool:
    """
    Check if a token has been revoked.

    Args:
        token: Token to check

    Returns:
        True if token is revoked, False otherwise
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_id = payload.get("jti")
        return token_id in revoked_tokens if token_id else False
    except JWTError:
        return True
