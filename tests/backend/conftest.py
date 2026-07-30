import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    original_state = {
        name: {
            key: value.copy() if isinstance(value, list) else value
            for key, value in activity.items()
        }
        for name, activity in activities.items()
    }

    try:
        yield TestClient(app)
    finally:
        activities.clear()
        activities.update(
            {
                name: {
                    key: value.copy() if isinstance(value, list) else value
                    for key, value in activity.items()
                }
                for name, activity in original_state.items()
            }
        )
