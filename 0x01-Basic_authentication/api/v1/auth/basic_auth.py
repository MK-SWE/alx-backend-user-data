#!/usr/bin/env python3
"""
Basic auth module for the API
"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ Decode Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            auth = base64_authorization_header.encode('utf-8')
            auth = base64.b64decode(auth)
            return auth.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ extract_user_credentials
        """
        if decoded_base64_authorization_header is None:
            return None
        if not isinstance(decoded_base64_authorization_header, str):
            return None
        if ":" not in decoded_base64_authorization_header:
            return None
        email, password = decoded_base64_authorization_header.split(":")
        return (email, password)
