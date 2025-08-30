
## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project demonstrates how to structure a FastAPI application with best practices for security, routing, and modularity. It is designed to be a starting point for building scalable and maintainable APIs using FastAPI.

## Features

- Modular project structure
- Secure authentication and authorization
- RESTful routing
- Environment-based configuration
- Easy-to-extend architecture

## Project Structure

```
RAG-FastApi/
├── app_new/
│   ├── main.py
│   ├── routers/
│   ├── templates/
├── config.py
└── database.py
├── requirements.txt
└── README.md
```

- **main.py**: Entry point for the FastAPI app.
- **routers/**: Contains route definitions.
- **models/**: Database models.


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/vikassrivastava18/FastAPI-Study.git
    cd FastAPI-Study
    ```
2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

- `GET /items/`: List items
- `POST /items/`: Create a new item
- `GET /users/me`: Get current user (requires authentication)

See the interactive docs at `/docs` (Swagger UI) and `/redoc`.

## Security

- JWT-based authentication
- Password hashing


## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.
