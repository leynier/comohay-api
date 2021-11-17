from apis.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_mock():
    assert True
