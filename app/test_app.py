import pytest
import app
from app import create_app
import flask.testing

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({'TESTING': True})
    yield app

@pytest.fixture()
def client(app):
    print(app.url_map)
    return app.test_client()

def test_get(client):
    response = client.get("/tubes")
    assert response.status == 200
