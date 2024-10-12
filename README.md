# The Late Show Flask API

This is a Flask-based RESTful API for managing episodes, guests, and appearances on "The Late Show." It supports CRUD operations and relational data using PostgreSQL.

## Features

- **Models:** Episodes, Guests, Appearances
- **Relationships:** 
  - An `Episode` has many `Guests` through `Appearance`
  - A `Guest` has many `Episodes` through `Appearance`
  - An `Appearance` belongs to an `Episode` and a `Guest`
- **Validations:** 
  - `Appearance` must have a rating between 1 and 5

## Endpoints

- **GET /episodes** - List all episodes
- **GET /episodes/:id** - Get details of a specific episode
- **GET /guests** - List all guests
- **POST /appearances** - Create a new appearance with validations

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/username/repo-name.git
   cd repo-name

2. **Create and set up the environment:**
    Open the .env file and update the DATABASE_URL variable with your PostgreSQL credentials:
    Example:
    DATABASE_URL=postgresql://username:password@localhost:5432/database_name
    
    
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Run migrations:**
    ```bash
    flask db upgrade

5. **Seed the database:**
    ```bash
    python seed.py

6. **Start the server:**
    ```bash
    flask run --port=5555

**Note: Ensure you have PostgreSQL installed and properly configured on your local machine or server.**