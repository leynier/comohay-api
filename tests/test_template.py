from fastapi.testclient import TestClient

from apis.main import app

client = TestClient(app)


def test_mock():
    assert True
