# Simple Social Media 

## Overview

This project is a simple social media application built using FastAPI. It simulates basic functionalities of a social media platform, including user management, content posting, and interactions such as liking posts. This API is designed to demonstrate the use of modern tools and practices in building scalable web applications.

## Features

- User Registration: Allows new users to register.
- User Login: Supports user authentication using JWT tokens.
- Create Posts: Authenticated users can create posts.
- Like Posts: Users can like posts.
- CRUD Operations: Supports create, read, update, and delete operations for users and posts.

## Technology Stack

- Python: The primary programming language used.
- FastAPI: Utilized for creating APIs due to its high performance and easy-to-use features.
- JWT (JSON Web Tokens): Used for secure user authentication.
- PostgreSQL: Used as the backend database to store all application data.
- Pydantic: Used for data validation and settings management using Python type annotations.
- SQLAlchemy: ORM tool used to interact with the database.
- Alembic: Handles database migrations and complements SQLAlchemy by providing database schema migrations.
- Pytest: For unit testing, making use of fixtures, parameterized tests, and a conftest file to manage test configurations.

## Getting Started

### Prerequisites

Ensure you have Python and PostgreSQL installed on your machine. Python 3.10 or higher is recommended. You will also need pip for installing Python packages and conda to create virtual environment.

### Installation

1. Clone the repository

```
git clone https://github.com/kumarrohit26/social-media-app-fastapi.git

cd social-media-app-fastapi
```

2. Set up a virtual environment (optional but recommended)

```
conda create -p venv python=3.10

conda activate venv/
```

3. Install the requirements
```
pip install -r requirements.txt
```

4. Set up the database

- Make sure PostgreSQL is running.
- Create a database named social_media.
- Run the migrations:

```
alembic upgrade head
```

5. Environment Variables

- Create a .env file in the project root.
- Add the following variables:

```
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = <your_database_password>
DATABASE_NAME = social_media
DATABASE_USERNAME = postgres
SECRET_KEY = <random_secret_key>
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
```

## Running the Application

```
uvicorn app.main:app --reload
```

## Running Tests

```
pytest --disable-warnings -v -x     # you can modify flags according to requirements.
```
## Usage

Navigate to http://localhost:8000/docs to view the Swagger UI that FastAPI generates, which provides a straightforward way to test the API endpoints.