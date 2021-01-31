# Utils.py

from kurellaz.env_vars import SALT
from passlib.hash import pbkdf2_sha256

# salting the password
def hash_password(password):
    return pbkdf2_sha256.hash(SALT + password)

def check_password(password, hashed):
    return pbkdf2_sha256.verify(SALT + password, hashed)

