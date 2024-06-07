#!/usr/bin/env python3
"""Module of session authenticating views.
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from os import getenv
from typing import Tuple


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """ Authenticate the user
    """
    email = request.form.get('email')
    pwd = request.form.get('password')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    if pwd is None or len(pwd.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if user.is_valid_password(pwd):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(user, 'id'))
        session = jsonify(user.to_json())
        session.set_cookie(getenv("SESSION_NAME"), session_id)
        return session
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """ Logout User
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})