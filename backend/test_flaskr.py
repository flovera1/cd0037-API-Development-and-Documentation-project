import json
import os
import unittest

from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.database_path = "sqlite:///trivia_test.db"

        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            c1 = Category(type="Science")
            db.session.add(c1)
            db.session.commit()

            # 🔥 THIS LINE IS MISSING
            self.category_id = c1.id

            q = Question(
                question="Test question?",
                answer="Test answer",
                difficulty=1,
                category=str(c1.id)
            )
            q.insert()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client.get('/categories')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']) >= 0)

    def test_get_questions(self):
        res = self.client.get('/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)

    def test_delete_nonexistent_question(self):
        res = self.client.delete('/questions/9999')
        self.assertEqual(res.status_code, 404)

    def test_create_question(self):
        new_question = {
            "question": "Test question?",
            "answer": "Test answer",
            "difficulty": 1,
            "category": 1
        }

        res = self.client.post('/questions', json=new_question)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


   

    def test_search_questions(self):
        res = self.client.post('/questions', json={
            "searchTerm": "Test"
        })
        print(res)

    #     print(res)
    #     data = res.get_json()

    #     print(data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertIn('questions', data)




    def test_get_questions_by_category(self):
        res = self.client.get(f'/categories/{self.category_id}/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_play_quiz(self):
        res = self.client.post('/quizzes', json={
            "previous_questions": [],
            "quiz_category": {"id": 0}
        })
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
