#!/usr/bin/env python3
"""DataBase module
"""
import requests


url = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """register_user endpoint unittest
    """
    payload = {'email': email, 'password': password}
    res = requests.post(f'{url}/users', data=payload)
    if res.status_code == 200:
        assert (res.json() == {"email": email, "message": "user created"})
    else:
        assert (res.status_code == 400)
        assert (res.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """log_in_wrong_password endpoint unittest
    """
    payload = {'email': email, 'password': password}
    res = requests.post(f'{url}/sessions', data=payload)
    assert (res.status_code == 401)


def log_in(email: str, password: str) -> str:
    """log_in endpoint unittest
    """
    payload = {'email': email, 'password': password}
    res = requests.post(f'{url}/sessions', data=payload)

    assert (res.status_code == 200)
    assert (res.json() == {"email": email, "message": "logged in"})
    assert (res.cookies["session_id"] is not None)
    return res.cookies["session_id"]


def profile_unlogged() -> None:
    """profile_unlogged endpoint unittest
    """
    res = requests.get(f'{url}/profile')
    assert (res.status_code == 403)


def profile_logged(session_id: str) -> None:
    """profile_logged endpoint unittest
    """
    res = requests.get(f'{url}/profile', cookies={"session_id": session_id})
    assert (res.status_code == 200)
    assert (res.json() == {"email": EMAIL})


def log_out(session_id: str) -> None:
    """log_out endpoint unittest
    """
    res = requests.delete(f'{url}/sessions',
                          cookies={"session_id": session_id})
    if res.status_code == 302:
        assert (res.url == 'http://127.0.0.1:5000/')
    else:
        assert (res.status_code == 200)


def reset_password_token(email: str) -> str:
    """reset_password_token endpoint unittest
    """
    res = requests.post(f'{url}/reset_password', data={"email": email})
    if res.status_code == 200:
        token = res.json()['reset_token']
        return token
    assert (res.status_code == 403)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update_password endpoint unittest
    """
    payload = {"email": email,
               "reset_token": reset_token,
               "new_password": new_password}
    res = requests.put(f'{url}/reset_password', data=payload)
    if res.status_code == 200:
        assert (res.json() == {"email": email, "message": "Password updated"})
    else:
        assert (res.status_code == 403)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
