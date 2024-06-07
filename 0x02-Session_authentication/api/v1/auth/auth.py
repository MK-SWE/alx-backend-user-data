#!/usr/bin/env python3
"""
Auth module for the API
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    The template for all authentication system will be implemented
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False - path and excluded_paths will be used later
        """
        if path is None or excluded_paths is None or len(excluded_paths) < 1:
            return True
        if excluded_paths[0][-1] == '*':
            if path.startswith(excluded_paths[0][0:-1]):
                return False
        if path in excluded_paths or path + "/" in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """  returns None - request will be the Flask request object
        """
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None - request will be the Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request:
        """
        if request is not None:
            return request.cookies.get(getenv('SESSION_NAME'))
        return request
