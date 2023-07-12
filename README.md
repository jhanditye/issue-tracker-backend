
# Issue Tracker App - Backend

The backend of the Issue Tracker App provides the API endpoints and database management for the app using FastAPI. It handles user authentication, project creation, and issue management functionalities.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/issue-tracker-backend.git
```

2. Navigate to the project directory:

```bash
cd issue-tracker-backend
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Set up the database:

- Update the database connection settings in the `.env` file.

5. Start the backend server:

```bash
uvicorn app.main:app --reload
```

The backend server will start running at `http://localhost:8000`.

## API Documentation

The API documentation is available at `http://localhost:8000/docs`. You can explore the available endpoints, view request/response schemas, and test the API using the interactive documentation.

## Endpoints

The following endpoints are available:

- `POST /api/register`: Register a new user.
- `POST /api/login`: Log in and obtain an access token.
- `GET /api/projects`: Retrieve a list of projects.
- `POST /api/projects`: Create a new project.
- `GET /api/projects/{id}`: Retrieve details of a specific project.
- `PUT /api/projects/{id}`: Update an existing project.
- `DELETE /api/projects/{id}`: Delete a project.
- `GET /api/issues`: Retrieve a list of issues.
- `POST /api/issues`: Create a new issue.
- `GET /api/issues/{id}`: Retrieve details of a specific issue.
- `PUT /api/issues/{id}`: Update an existing issue.
- `DELETE /api/issues/{id}`: Delete an issue.

## Technologies Used

- Python
- FastAPI
- PostgreSQL

