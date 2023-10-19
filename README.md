# Flask User Authentication Backend

This Flask-based backend service provides user authentication features, including registration and login endpoints. It's designed to work with a PostgreSQL database and includes password hashing for security. This backend service can serve as the authentication foundation for your Flask-based applications.

## Features

- User registration with name, email, and password.
- Passwords are securely hashed before storing in the database.
- User login with email and password.
- Protected routes that require user authentication.
- PostgreSQL database integration.

## Installation and Setup

1. Install the required dependencies listed in `requirements.txt`:

   ```shell
   pip install -r requirements.txt
