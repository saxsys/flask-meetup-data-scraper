from datetime import datetime
from time import sleep

import pytest
from flask.app import Flask

from app import create_app
from meetup_search.commands.migrate_models import migrate_models
from meetup_search.meetup_api_client.meetup_api_client import MeetupApiClient
from meetup_search.models.group import Group
from meetup_search.models.meetup_zip import MeetupZip
from meetup_search.models.token import Token


@pytest.fixture
def api_client() -> MeetupApiClient:
    """
    meetup api client

    Returns:
        MeetupApiClient -- Meetup Api client
    """
    return MeetupApiClient()


@pytest.fixture
def app() -> Flask:
    """
    flask app fixture for texting

    Returns:
        Flask -- flask app with testing config
    """
    return create_app(config_path="/app/config/test.py")


@pytest.fixture
def meetup_groups() -> dict:
    """
    test groups with id & real meetup group urlname

    Returns:
        dict -- dict with mutiple meetup groups
    """
    return {
        "sandbox": {"meetup_id": 1556336, "urlname": "Meetup-API-Testing"},
        "not-exist": {"meetup_id": 123456, "urlname": "None"},
        "gone": {"meetup_id": 654321, "urlname": "connectedawareness-berlin"},
    }


def create_group(
    urlname: str, meetup_id: int = 0, name: str = "", lat: float = 0, lon: float = 0
) -> Group:
    """
    create group object 

    Arguments:
        urlname {str} -- urlname for group object

    Keyword Arguments:
        meetup_id {int} -- meetup_id for group object (default: {0})
        name {str} -- name for group object (default: {""})

    Returns:
        Group -- new unsaved group object
    """

    return Group(
        meetup_id=meetup_id,
        urlname=urlname,
        created=datetime.now(),
        description="",
        name=name,
        link="",
        location={"lat": lat, "lon": lon},
        members=0,
        status="",
        timezone="",
        visibility="",
    )


@pytest.fixture
def group_1() -> Group:
    """
    create group object

    Returns:
        Group -- unsaved group object
    """
    return create_group(urlname="1")


@pytest.fixture
def group_2() -> Group:
    """
    create group object with a differnet urlname than group_1

    Returns:
        Group -- unsaved group object
    """
    return create_group(urlname="2")

@pytest.fixture
def auth_token() -> Token:
    """
    create new token
    
    Returns:
        Token -- saved token
    """

    new_token: Token = Token(
        access_token="access",
        refresh_token="refresh"
        )

    return new_token

def pytest_runtest_setup():
    """
    Run for each test

    delete elasticsearch index & init the index afterwards
    """
    delte_index()
    init_models()


def pytest_runtest_teardown():
    """
    Run after each test

    delete elasticsearch index
    """
    delte_index()


def delte_index():
    """
    delte elasticsearch index
    """
    print("delete Elasticsearch index: {}".format(Group.Index.name))
    create_app(config_path="/app/config/test.py").config["ES"].indices.delete(
        index=Group.Index.name, ignore=[400, 404]
    )

    print("delete Elasticsearch index: {}".format(MeetupZip.Index.name))
    create_app(config_path="/app/config/test.py").config["ES"].indices.delete(
        index=MeetupZip.Index.name, ignore=[400, 404]
    )

    print("delete Elasticsearch index: {}".format(Token.Index.name))
    create_app(config_path="/app/config/test.py").config["ES"].indices.delete(
        index=Token.Index.name, ignore=[400, 404]
    )

    sleep(2)


def init_models():
    """
    init elasticsearch index
    """
    migrate_models()
    sleep(1)
