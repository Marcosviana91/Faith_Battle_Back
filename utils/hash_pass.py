from passlib.hash import argon2

def encrypt(password: str):
    return argon2.hash(password)

def verify(password: str, encrypted_password: str):
    return argon2.verify(password, encrypted_password)