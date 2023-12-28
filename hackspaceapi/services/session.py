import requests

from hackspaceapi import VERSION


def get_requests_session() -> requests.Session:
    """
    Creates a Requests session pre-configured with the common values used by
    all outbound requests
    """
    session = requests.session()
    session.headers = {"User-Agent": "HackspaceAPI/{0}".format(VERSION)}

    return session
