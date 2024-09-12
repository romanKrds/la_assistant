# Language Learning Assistant - Flask App

This Flask application is designed to help users study foreign languages. The app provides a base for an interactive platform where users can communicate with an AI assistant to improve their language skills.

## Features

- **Vocabulary acquisition**: Users can learn new words and review them for the better memorization.

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Setting Up the Development Environment](#setting-up-the-development-environment)
4. [Running the Application](#running-the-application)
5. [Database Migrations](#database-migrations)
6. [Running Tests](#running-tests)

## Requirements

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/main/#installing-with-the-official-installer) (for dependency management)
- [Docker](https://www.docker.com/) (for database setup)

## Installation

Clone the repository and install dependencies using Poetry.

```bash
git clone https://github.com/romanKrds/la_assistant.git
cd la_assistant
poetry install
```

## Setting Up the Development Environment

### 1. Configure Environment Variables

Create a `.env` file in the root of your project directory with the following content.

```env
FLASK_ENV=development
REPETITIONS_TO_MEMORIZE_WORD_NUMBER=10
MEMORIZE_WORD_SET_LENGTH=10
```

Create a `.env.mysql.env` file in the root of your project directory with the following content.

```env
MYSQL_HOST='localhost'
MYSQL_DATABASE='la_assistant_db'
MYSQL_USER='la_assistant_db_user'
MYSQL_PASSWORD='<set_user_password_here>'
MYSQL_ROOT_PASSWORD='<set_root_user_password_here>'
```

### 2. Set Up the MySQL Database Using Docker

Run the following command to start a MySQL server using Docker.

```bash
docker compose up
```

### 3. Initialize the Database

Once your Docker container is running, initialize the database using Flask-Migrate.

```bash
# Optional, check if Docker container is running (by status)
docker ps 

# Apply migrations
flask db upgrade
```

## Running the Application

To run the application locally:

1. **Install dependencies:**

   ```bash
   poetry install
   ```

2. **Activate the Virtual Environment:**

   ```bash
   poetry shell
   ```

3. **Migrate DB:**

   ```bash
   flask db upgrade
   ```

4. **Populate DB with data:**

   ```bash
   flask --app la_assistant populate-db
   ```

5. **Run the Application:**

   ```bash
   flask run
   ```

This will start the Flask application on `http://127.0.0.1:5000/`. You should see your application running if you navigate to this URL in your browser.


## Database Migrations

Flask-Migrate helps you manage database schema changes. Here’s how to handle migrations:

1. **Create a New Migration:**

   Whenever you make changes to your models, create a new migration to reflect those changes in the database schema.

   ```bash
   flask db migrate -m "Description of changes"
   ```

2. **Apply Migrations:**

   Apply the migrations to update the database schema.

   ```bash
   flask db upgrade
   ```

3. **Downgrade Migrations:**

   If needed, you can also downgrade (revert) migrations.

   ```bash
   flask db downgrade
   ```

## Running Tests

Tests are essential for maintaining code quality and ensuring that changes do not break existing functionality. Here’s how to run tests:

1. **Activate the Virtual Environment:**

   If not already activated:

   ```bash
   poetry shell
   ```

2. **Run Tests with pytest:**

   Run all tests:

   ```bash
   pytest
   ```

   To run tests in a specific file or directory:

   ```bash
   pytest path/to/test_file.py
   ```

   For more detailed output, you can use:

   ```bash
   pytest -v
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.