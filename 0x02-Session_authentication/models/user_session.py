#!/usr/bin/env python3
""" UserSession module
"""
from models.base import Base

class UserSession(Base):
    """ UserSession database storage
    """
    def __init__(self, user_id, session_id):
        pass