#!/usr/bin/env python3
"""
Session db module for the API
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


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
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None

    def destroy_session(self, request=None):
        """ Overload destroy_session function
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
