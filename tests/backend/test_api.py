from urllib.parse import quote


def test_list_activities_returns_the_activity_catalog(client):
    # Arrange
    # No setup needed for the catalog endpoint.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["max_participants"] == 12


def test_signup_for_activity_adds_a_new_participant(client):
    # Arrange
    email = "new-student@example.com"

    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"


def test_signup_prevents_duplicate_registration(client):
    # Arrange
    email = "duplicate-student@example.com"
    client.post(f"/activities/Chess Club/signup?email={email}")

    # Act
    duplicate_response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert duplicate_response.status_code == 400
    assert "already signed up" in duplicate_response.json()["detail"].lower()


def test_unregister_participant_removes_the_student(client):
    # Arrange
    email = "remove-me@example.com"
    client.post(f"/activities/Chess Club/signup?email={email}")

    # Act
    unregister_response = client.delete(f"/activities/Chess Club/participants/{quote(email)}")

    # Assert
    assert unregister_response.status_code == 200
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]
