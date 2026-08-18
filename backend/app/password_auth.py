"""Stateless single-password authentication."""

from hashlib import sha256
from hmac import compare_digest, new as new_hmac

from itsdangerous import BadSignature, URLSafeSerializer

from app.settings import settings


TOKEN_SALT = "inkforge-password-auth"
TOKEN_PAYLOAD = "authenticated"


def is_password_auth_enabled() -> bool:
    return bool(settings.password)


def password_matches(candidate: str) -> bool:
    expected = settings.password
    if not expected:
        return False
    return compare_digest(candidate.encode("utf-8"), expected.encode("utf-8"))


def issue_access_token() -> str:
    return _serializer().dumps(TOKEN_PAYLOAD)


def verify_access_token(token: str | None) -> bool:
    if not is_password_auth_enabled():
        return True
    if not token:
        return False
    try:
        return _serializer().loads(token) == TOKEN_PAYLOAD
    except BadSignature:
        return False


def extract_bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    scheme, separator, token = authorization.partition(" ")
    if not separator or scheme.lower() != "bearer" or not token:
        return None
    return token


def _serializer() -> URLSafeSerializer:
    password = settings.password
    if not password:
        raise RuntimeError("Password authentication is not enabled")
    signing_key = new_hmac(
        settings.encryption_key.encode("utf-8"),
        password.encode("utf-8"),
        sha256,
    ).digest()
    return URLSafeSerializer(signing_key, salt=TOKEN_SALT)
