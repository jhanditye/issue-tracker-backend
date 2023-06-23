# Issue Tracker Backend

This repository houses the backend services for the Issue Tracker application. It's built using Node.js with Express, and employs a PostgreSQL database to store user data.

## Features

- User Registration and Login
- JSON Web Token (JWT) Authentication
- PostgreSQL Database Integration

## Installation

To run this project locally, follow these steps:

1. Clone the repository: 
    ```
    git clone https://github.com/jhanditye/issue-tracker-backend.git
    ```
2. Install dependencies: 
    ```
    npm install
    ```
3. Set up your environment variables in a `.env` file in the root directory. You'll need to define:
    - `DATABASE_URL` - Your PostgreSQL connection string
    - `JWT_SECRET` - A secret key for signing JWTs
4. Run the project: 
    ```
    npm start
    ```

## API Endpoints

- `POST /register`: Register a new user. Expects JSON in the format `{ "username": "user", "password": "password", "email": "user@example.com" }`.
- `POST /login`: Authenticate a user. Expects JSON in the format `{ "username": "user", "password": "password" }`.

## Contact

If you encounter any issues or have questions about this project, feel free to reach out or open an issue.

**Note:** As this project is still in development, more features and documentation will be added over time.
Now, you can copy and paste this into yo