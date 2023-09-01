# Issue Tracker Backend with FastAPI

This project provides backend support for an issue tracker application, using FastAPI. Features include user authentication, issue handling, and user management.

## Table of Contents

- [Endpoints](#endpoints)
  - [Authentication](#authentication)
  - [Issues](#issues)
  - [Users](#users)
- [Setup and Running](#setup-and-running)
  - [Requirements](#requirements)
  - [Instructions](#instructions)

## Endpoints

### Authentication

- `POST /login`: Authenticate user and retrieve an access token.

### Issues

- `GET /issues`: List issues with an optional search query.
- `POST /issues`: Create a new issue.
- `GET /issues/{id}`: Fetch a specific issue using its ID.
- `DELETE /issues/{id}`: Delete a specific issue by ID.
- `PUT /issues/{id}`: Update details of a specific issue by ID.

### Users

- `POST /users`: Register a new user.

## Setup and Running

### Requirements

- Docker
- Docker Compose

### Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/jhanditye/issue-tracker-backend.git
   ```

2. **Configure Environment**

   Create a `.env` file in the root directory and populate it with the necessary configurations(database config).

3. **Run the Application with Docker Compose**

   ```bash
   docker-compose -f docker-compose-dev.yml up
   ```

This starts the FastAPI application on port 8001 and initializes a PostgreSQL database.
