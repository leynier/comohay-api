from fastapi.testclient import TestClient

from comohay_api.main import app

client = TestClient(app)


def test_mock():
    assert True
