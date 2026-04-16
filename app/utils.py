from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==============================
# HASH PASSWORD (SAFE FIX)
# ==============================
def hash_password(password: str):
    # ✅ Step 1: Convert to SHA256 (removes bcrypt 72-byte limit issue)
    password = hashlib.sha256(password.encode()).hexdigest()
    
    # ✅ Step 2: Hash using bcrypt
    return pwd_context.hash(password)


# ==============================
# VERIFY PASSWORD
# ==============================
def verify_password(plain_password: str, hashed_password: str):
    # ✅ Apply same SHA256 before verifying
    plain_password = hashlib.sha256(plain_password.encode()).hexdigest()
    
    return pwd_context.verify(plain_password, hashed_password)