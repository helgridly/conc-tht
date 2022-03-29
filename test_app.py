import pytest
from app import create_app, db, TubeStatus

@pytest.fixture()
def app():
    app = create_app("sqlite:///")
    app.config.update({"TESTING": True})
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture(scope="function", autouse=True)
def fresh_db(app):
    """Empty the database of all data between tests."""
    with app.app_context():
        db.create_all()
    yield
    with app.app_context():
        db.drop_all()

def test_get(client):
    resp = client.get("/tubes")
    assert resp.status_code == 200
    assert type(resp.json) == list

def test_newtube(client):
    # request a new tube
    r_new = client.post("/tubes", json={"patient_email": "foo@bar.baz"})
    assert r_new.status_code == 200
    assert "barcode" in r_new.json
    assert "status" in r_new.json and r_new.json["status"] == "registered"

    # should get it back
    r_get = client.get("/tubes")
    assert r_get.status_code == 200
    assert r_get.json == [r_new.json]

def test_newtube_bademail(client):
    # not a valid email
    resp = client.post("/tubes", json={"patient_email": "foo#bar.baz"})
    assert resp.status_code == 400

@pytest.mark.parametrize("target_status", [e.name for e in TubeStatus])
def test_tubestatus_update(client, target_status):
    """paramaterized test: tests all statuses"""
    r_new = client.post("/tubes", json={"patient_email": "foo@bar.baz"})

    # update status to target
    update_json = {"barcode": r_new.json["barcode"], "status": target_status}
    r_update = client.patch("/tubes", json=update_json)
    assert r_update.status_code == 200
    assert r_update.json == update_json

    # shouldn't show up in /get unless registered
    r_get = client.get("/tubes")
    assert r_get.status_code == 200
    assert (target_status != "registered") == (r_get.json == [])

def test_bad_tubestatus(client):
    r_new = client.post("/tubes", json={"patient_email": "foo@bar.baz"})

    # update status to nonexistent status
    update_json = {"barcode": r_new.json["barcode"], "status": "NotARealStatus"}
    r_update = client.patch("/tubes", json=update_json)
    assert r_update.status_code == 400

