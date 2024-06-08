#!/usr/bin/env python3
"""
Session expiration auth module for the API
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import (
    datetime,
    timedelta
)


class SessionExpAuth(SessionAuth):
    """
    Implement session expiration mechanizem
    """
    def __init__(self):
        """Init the class"""
        try:
            session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """Create a session with experation"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID:
        """
        if session_id is None:
            return None
        user = self.user_id_by_session_id.get(session_id)
        if user is None:
            return None
        if "created_at" not in user.keys():
            return None
        if self.session_duration <= 0:
            return user.get("user_id")
        created_at = user.get("created_at")
        session_expiry = created_at + timedelta(seconds=self.session_duration)
        if session_expiry < datetime.now():
            return None
        return user.get("user_id")
