import pytest
import json
from unittest.mock import patch
from datetime import datetime
from .utils import client, test_db


def test_add_task(test_db):
    mutation = """
    mutation {
        addTask(title:"New Task") {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    data = mock_utcnow_and_execute(mutation)

    assert data["data"]["addTask"]["id"] == "3"
    assert data["data"]["addTask"]["title"] == "New Task"
    assert data["data"]["addTask"]["createdAt"] == "2023-01-05T09:00:00"
    assert data["data"]["addTask"]["completed"] is False
    assert data["data"]["addTask"]["updatedAt"] is None


def test_add_task_with_invalid_input(test_db):
    mutation = """
    mutation {
        addTask(title:"") {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200

    data = response.json()
    assert data["data"] is None
    assert data['errors'][0]['message'] == "Title cannot be empty"


def test_toggle_task(test_db):
    mutation = """
    mutation {
        toggleTask(id:1) {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    data = mock_utcnow_and_execute(mutation)

    assert data["data"]["toggleTask"]["id"] == "1"
    assert data["data"]["toggleTask"]["completed"] is True
    assert data["data"]["toggleTask"]["updatedAt"] == "2023-01-05T09:00:00"


def test_toggle_task_with_invalid_input(test_db):
    mutation = """
    mutation {
        toggleTask(id:-2) {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200

    data = response.json()
    assert data["data"] is None
    assert data['errors'][0]['message'] == "Invalid task ID: must be a positive integer."


def test_toggle_not_found_task(test_db):
    mutation = """
    mutation {
        toggleTask(id:4) {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200

    data = response.json()
    assert data["data"] is None
    assert data['errors'][0]['message'] == "Task with id 4 not found"


def test_edit_task(test_db):
    mutation = """
    mutation {
        editTask(id:2, title:"Edited Test Task 2") {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    data = mock_utcnow_and_execute(mutation)

    assert data["data"]["editTask"]["id"] == "2"
    assert data["data"]["editTask"]["title"] == "Edited Test Task 2"
    assert data["data"]["editTask"]["updatedAt"] == "2023-01-05T09:00:00"


@pytest.mark.parametrize("input_data, expected_error_message", [
    ({"id": -1, "title": "New Test Task"}, "Invalid task ID: must be a positive integer."),
    ({"id": 2, "title": " "}, "Title cannot be empty"),
])
def test_edit_task_with_invalid_inputs(test_db, input_data, expected_error_message):
    input_string = ', '.join(f'{k}: {json.dumps(v)}' for k, v in input_data.items())

    mutation = f"""
    mutation {{
        editTask({input_string}) {{
            id
            title
            completed
            createdAt
            updatedAt
        }}
    }}
    """

    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200

    data = response.json()
    assert data["data"] is None
    assert data['errors'][0]['message'] == expected_error_message


def test_edit_not_found_task(test_db):
    mutation = """
    mutation {
        editTask(id:4, title:"Not found Task") {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200

    data = response.json()
    assert data["data"] is None
    assert data['errors'][0]['message'] == "Task with id 4 not found"


def test_delete_task(test_db):
    mutation = """
    mutation {
        deleteTask(id:2) {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200

    data = response.json()
    assert data["data"]["deleteTask"]["id"] == "2"


def test_delete_task_with_invalid_input(test_db):
    mutation = """
    mutation {
        deleteTask(id:-100) {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200

    data = response.json()
    assert data["data"] is None
    assert data['errors'][0]['message'] == "Invalid task ID: must be a positive integer."


def test_delete_not_found_task(test_db):
    mutation = """
    mutation {
        deleteTask(id:5) {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200

    data = response.json()
    assert data["data"] is None
    assert data['errors'][0]['message'] == "Task with id 5 not found"


def mock_utcnow_and_execute(mutation, fixed_datetime=datetime(2023, 1, 5, 9, 0, 0)):
    with patch("schema.datetime") as mock_datetime:
        mock_datetime.utcnow.return_value = fixed_datetime
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        response = client.post("/graphql", json={"query": mutation})
        assert response.status_code == 200

        return response.json()
