#!/usr/bin/env python3
"""
Basic auth module for the API
"""
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
        The class that manage the session authentication mechanism
    """
