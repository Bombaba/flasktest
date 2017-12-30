import base64
import hashlib
import secrets

def get_hash(plain):
    return hashlib.sha512(plain.encode('ascii')).hexdigest()

def get_salt():
    return base64.b64encode(secrets.token_bytes(20)).decode('ascii')

def validate_password(plain, salt, expected):
    return get_hash(plain + salt) == expected