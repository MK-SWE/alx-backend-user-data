#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union

from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register the user
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate user credentials
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create Session
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Distroy session
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

    def get_user_from_session_id(self, session_id: str) -> Union[None, User]:
        """Find user by session ID
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user


def _hash_password(password: str) -> bytes:
    """Create new hashed password using bcrypt
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate UUIDs
    """
    return str(uuid4())
