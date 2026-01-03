import pytest
from fastapi.testclient import TestClient
from demo import app



class FakeDB:
    def get_users(self):
        return []
    

@pytest.fixture
def client():
    return TestClient(app)

def test_users(client):
    response=client.get("/test/Test")

    db=FakeDB()
    data=db.get_users()
    data.append({
        'id':'1',
        'name':'Test'
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Test"

