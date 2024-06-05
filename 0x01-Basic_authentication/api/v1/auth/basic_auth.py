#!/usr/bin/env python3
"""
Basic auth module for the API
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    The template for basic authentication module
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract the Base64 encoded characters
        """
        if authorization_header is None:
            return None
        if isinstance(authorization_header, str):
            if authorization_header[0:6] != "Basic ":
                return None
            return authorization_header[6:]
        else:
            return None
