#!/usr/bin/env python3
"""Auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Create new hashed password using bcrypt
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
