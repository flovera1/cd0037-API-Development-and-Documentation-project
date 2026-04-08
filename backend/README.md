# Backend - Trivia API
This is an API backend project for a trivia game app developed using Flask framework. This app enables users to view the questions, sort by category, create new questions, delete old questions, search questions and play the quiz game.

This project has been developed as a requirement for the Udacity API Development & Documentation course.

## Getting Started
Prerequisites
  - Python 3.x
  - pip
  - (Optional) virtual environment

Create and activate a virtual environment (optional but recommended):

  - python -m venv venv
  - venv\Scripts\activate   # Windows

Install dependencies:

  - pip install -r requirements.txt

## Database Setup

This project uses SQLite instead of PostgreSQL due to environment constraints (Python 3.14 compatibility and system restrictions).

SQLite is fully supported by SQLAlchemy and provides identical functionality for this application.

All endpoints, queries, and tests behave as expected.

The database is automatically created when the server starts:

sqlite:///trivia.db

No additional setup is required.

The database is automatically created when the server starts:

sqlite:///trivia.db

No additional setup is required.

API Endpoints
GET /categories

Returns all available categories.

Response:

{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art"
  }
}
GET /questions

Returns paginated questions (10 per page).

Query params:

page (int)

Response:

{
  "success": true,
  "questions": [...],
  "totalQuestions": 20,
  "categories": {...},
  "currentCategory": null
}
DELETE /questions/<id>

Deletes a question.

Response:

{
  "success": true,
  "deleted": 5
}
POST /questions

Handles both creating and searching questions.

Create a question

Request:

{
  "question": "What is AI?",
  "answer": "Artificial Intelligence",
  "difficulty": 2,
  "category": 1
}

Response:

{
  "success": true,
  "created": 10
}
Search questions

Request:

{
  "searchTerm": "title"
}

Response:

{
  "success": true,
  "questions": [...],
  "totalQuestions": 3,
  "currentCategory": null
}
GET /categories/<id>/questions

Returns questions for a specific category.

Response:

{
  "success": true,
  "questions": [...],
  "totalQuestions": 5,
  "currentCategory": "Science"
}
POST /quizzes

Returns a random question for the quiz.

Request:

{
  "previous_questions": [1, 2],
  "quiz_category": {"id": 1}
}

Response:

{
  "success": true,
  "question": {
    "id": 3,
    "question": "...",
    "answer": "...",
    "category": "1",
    "difficulty": 2
  }
}
Error Handling

Errors return JSON in this format:

{
  "success": false,
  "error": 404,
  "message": "resource not found"
}

Handled errors:

400 — Bad request
404 — Resource not found
422 — Unprocessable
500 — Internal server error
Testing

To run tests:

python test_flaskr.py

Tests cover both success and failure cases for each endpoint.