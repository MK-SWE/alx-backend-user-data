#!/usr/bin/env python3
"""
Auth module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    The template for all authentication system will be implemented
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False - path and excluded_paths will be used later
        """
        return False

    def authorization_header(self, request=None) -> str:
        """  returns None - request will be the Flask request object
        """
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None - request will be the Flask request object
        """
        return request
