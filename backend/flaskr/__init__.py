import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [q.format() for q in selection]
    return questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})

    with app.app_context():
        db.create_all()

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, DELETE, OPTIONS'
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()

        if len(categories) == 0:
            abort(404)

        formatted = {cat.id: cat.type for cat in categories}

        return jsonify({
            'success': True,
            'categories': formatted
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(selection) == 0:
            abort(404)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()
        formatted_categories = {c.id: c.type for c in categories}

        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(selection),
            'categories': formatted_categories,
            'currentCategory': None
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = db.session.get(Question, question_id)

        if question is None:
            abort(404)

        try:
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            }), 200

        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    and also handle search functionality.
    """
    @app.route('/questions', methods=['POST'])
    def create_or_search_question():
        body = request.get_json()

        if body is None:
            abort(400)

        # ---------------------------
        # SEARCH
        # ---------------------------
        if 'searchTerm' in body:
            search_term = body.get('searchTerm', '')

            results = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')
            ).all()

            current_questions = paginate_questions(request, results)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'totalQuestions': len(results),
                'currentCategory': None
            })

        # ---------------------------
        # CREATE
        # ---------------------------
        question = body.get('question')
        answer = body.get('answer')
        difficulty = body.get('difficulty')
        category = body.get('category')

        if not all([question, answer, difficulty, category]):
            abort(400)

        try:
            new_question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=str(category)  # FIX: ensure string
            )
            new_question.insert()

            return jsonify({
                'success': True,
                'created': new_question.id
            })

        except:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        category = db.session.get(Category, category_id)

        if category is None:
            abort(404)

        questions = Question.query.filter_by(
            category=str(category_id)
        ).all()

        current_questions = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(questions),
            'currentCategory': category.type
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()

        if body is None:
            abort(400)

        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category')

        if quiz_category and int(quiz_category.get('id')) != 0:
            questions = Question.query.filter_by(
                category=str(quiz_category.get('id'))  # FIX
            ).all()
        else:
            questions = Question.query.all()

        available_questions = [
            q for q in questions if q.id not in previous_questions
        ]

        if len(available_questions) == 0:
            return jsonify({
                'success': True,
                'question': None
            })

        question = random.choice(available_questions)

        return jsonify({
            'success': True,
            'question': question.format()
        })

    """
    @TODO:
    Create error handlers for all expected errors.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app