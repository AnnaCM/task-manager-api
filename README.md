# Task Manager GraphQL API
A basic GraphQL API server built using FastAPI, Strawberry GraphQL, SQLAlchemy, and Python to manage a simple list of tasks.

This project exposes a GraphQL endpoint to create, update, toggle, delete, and list tasks.

## Prerequisites
This app requires:
- Python 3.10+
- pip (Python package manager)

## Setup Instructions
1. Clone the repository
```bash
git clone git@github.com:AnnaCM/task-manager-api.git
cd task-manager-api
```

2. Create and activate a virtual environment
```bash
python3 -m venv venv

# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the API
Start the FastAPI server with:
```bash
uvicorn main:app --reload
```
This will start the FastAPI app with hot-reloading.

By default, the app will be available at:
```bash
http://127.0.0.1:8000/graphql
```
Open that URL in your browser to use the built-in Strawberry GraphQL Playground where you can run queries and mutations.

## Running tests
To run the tests for this project, use the following command from the root of the project:
```bash
python3 -m pytest
```
Make sure that you run the tests from the root directory of the project so that relative imports work correctly, and that your virtual environment is activated.

## Error Handling

Currently, the API handles errors by raising basic Python exceptions.

### Planned Improvements for Complex Error Handling

To better support frontend development and enable more user-friendly error messages, a structured error-handling approach can be introduced using Strawberry’s `GraphQLError` class along with custom `extensions`.

Key improvements:

- **Centralized Error Management**: Define reusable custom exceptions in a dedicated `errors.py` module, each with a unique error code and message.
- **Consistent Error Format**: Ensure that all GraphQL errors follow a consistent and predictable schema, for example:
  ```json
  {
    "errors": [
      {
        "message": "Task not found.",
        "extensions": {
          "code": "TASK_NOT_FOUND"
        }
      }
    ]
  }
  ```
- **Frontend Integration**: Error codes (e.g. `TASK_NOT_FOUND`, `INVALID_INPUT`) can be mapped to translated or user-friendly messages on the frontend.
- **Internationalization Support**: Error codes enable language-specific messaging without hardcoding messages on the backend.

## Notes
- The API uses a local SQLite database (tasks.db).
- Timestamps (created_at, updated_at) are stored as Unix timestamps (integers).
- In the GraphQL schema, timestamps are returned as proper DateTime types.

## License
This project is licensed under the terms of the [MIT License](LICENSE.md).
