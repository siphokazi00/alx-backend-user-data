#!/usr/bin/env python3
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password with bcrypt and return the hashed password."""
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the provided password matches the hashed password."""
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')

    # Check if the hashed password matches the provided password
    return bcrypt.checkpw(password_bytes, hashed_password)
