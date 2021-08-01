import base64

from flask_httpauth_without_orm import __version__
from flask_httpauth_without_orm.main import app
from requests import get
from requests.auth import HTTPBasicAuth


def test_version():
    assert __version__ == "0.1.0"


def test_unit_without_auth():
    """
    Test request to / without auth
    """
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 401


def test_unit_with_auth():
    """
    Test request to / with auth
    """
    with app.test_client() as client:
        token = base64.b64encode("username1:1234".encode("ascii")).decode("ascii")
        response = client.get("/", headers={"Authorization": f"Basic {token}"})
        assert response.status_code == 200


def integration_test_without_auth():
    response = get("http://127.0.0.1:5000")
    assert response.status_code == 401


def integration_test_with_auth():
    auth = HTTPBasicAuth("username1", "1234")
    response = get("http://127.0.0.1:5000", auth=auth)
    assert response.status_code == 200


if __name__ == "__main__":
    integration_test_without_auth()
    integration_test_with_auth()
