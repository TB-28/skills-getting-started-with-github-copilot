from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_prevents_duplicate_registration():
    email = "duplicate-test@example.com"

    first_response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert first_response.status_code == 200

    duplicate_response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert duplicate_response.status_code == 400
    assert "already signed up" in duplicate_response.json()["detail"].lower()


def test_unregister_participant_removes_from_activity():
    email = "remove-me@example.com"

    signup_response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/Chess Club/participants/{quote(email)}"
    )
    assert unregister_response.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]
