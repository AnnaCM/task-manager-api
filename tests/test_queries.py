import pytest
from .utils import client, test_db

def test_get_tasks(test_db):
    query = """
    query {
        tasks {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200

    data = response.json()
    assert "tasks" in data["data"]
    assert len(data["data"]["tasks"]) == 2

    assert data["data"]["tasks"][0]["id"] == "1"
    assert data["data"]["tasks"][0]["title"] == "Test Task 1"
    assert data["data"]["tasks"][0]["completed"] == False
    assert data["data"]["tasks"][0]["createdAt"] == "2023-01-01T12:00:00"
    assert data["data"]["tasks"][0]["updatedAt"] is None

    assert data["data"]["tasks"][1]["id"] == "2"
    assert data["data"]["tasks"][1]["title"] == "Test Task 2"
    assert data["data"]["tasks"][1]["completed"] == True
    assert data["data"]["tasks"][1]["createdAt"] == "2023-01-02T10:00:00"
    assert data["data"]["tasks"][1]["updatedAt"] == "2023-01-02T18:00:00"


def test_get_tasks_with_optional_argument(test_db):
    query = """
    query {
        tasks(search:"1") {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200

    data = response.json()
    assert "tasks" in data["data"]
    assert len(data["data"]["tasks"]) == 1
    assert data["data"]["tasks"][0]["title"] == "Test Task 1"


def test_get_task(test_db):
    query = """
    query {
        task(id:2) {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200

    data = response.json()
    assert "task" in data["data"]
    assert len(data["data"]) == 1
    assert data["data"]["task"]["id"] == "2"


def test_get_task_with_invalid_input(test_db):
    query = """
    query {
        task(id:0) {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200

    data = response.json()
    assert data["data"] is None
    assert data['errors'][0]['message'] == "Invalid task ID: must be a positive integer."


def test_get_not_found_task(test_db):
    query = """
    query {
        task(id:3) {
            id
            title
            completed
            createdAt
            updatedAt
        }
    }
    """

    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200

    data = response.json()
    assert data["data"] is None
    assert data['errors'][0]['message'] == "Task with id 3 not found"
