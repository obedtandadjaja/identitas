from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd.verify(password, hashsed_password)

def hash_password(password: str) -> str:
    return pwd.hash(password)
