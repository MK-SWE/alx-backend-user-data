#!/usr/bin/env python3
"""
Session auth module for the API
"""
from api.v1.auth.auth import Auth
from models.user import User
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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID:
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """ Return User object by id
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Delete session
        """
        session_id = self.session_cookie(request)
        user = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
