from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==============================
# 🔐 HASH PASSWORD (FIXED)
# ==============================
def hash_password(password: str):
    # bcrypt max length = 72 bytes
    password = password.encode("utf-8")[:72].decode("utf-8")
    return pwd_context.hash(password)


# ==============================
# 🔍 VERIFY PASSWORD
# ==============================
def verify_password(plain_password: str, hashed_password: str):
    plain_password = plain_password.encode("utf-8")[:72].decode("utf-8")
    return pwd_context.verify(plain_password, hashed_password)