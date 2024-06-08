#!/usr/bin/env python3
"""
Session db module for the API
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import (
    datetime,
    timedelta
)


class SessionDBAuth(SessionExpAuth):
    """ Store Session data in a database
    """
    def create_session(self, user_id=None):
        """ Overload the create_session function
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictonary = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**session_dictonary)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Overload user_id_for_session_id function
        """
        try:
            sessionData = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessionData) <= 0:
            return None
        currentTime = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        expire_time = sessionData[0].created_at + time_span
        if expire_time < currentTime:
            return None
        return sessionData[0].user_id

    def destroy_session(self, request=None):
        """ Overload destroy_session function
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        try:
            user_session = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(user_session) <= 0:
            return False
        user_session[0].remove()
        return True
