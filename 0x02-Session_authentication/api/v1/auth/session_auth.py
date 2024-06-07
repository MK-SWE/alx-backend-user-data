#!/usr/bin/env python3
"""
Basic auth module for the API
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
        The class that manage the session authentication mechanism
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Generate Session
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        Session_ID = str(uuid.uuid4())
        self.user_id_by_session_id[Session_ID] = user_id
        return Session_ID
