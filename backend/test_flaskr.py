import unittest

from flaskr import create_app
from models import db, Question, Category
from settings import TEST_DB_NAME


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.database_path = f"sqlite:///{TEST_DB_NAME}"

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

    
    def test_get_categories(self):
        res = self.client.get('/categories')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']) > 0)

    def test_get_categories_failure(self):
        res = self.client.get('/categoriezz')  # invalid route
        self.assertEqual(res.status_code, 404)

    
    def test_get_questions(self):
        res = self.client.get('/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)

    def test_get_questions_failure(self):
        res = self.client.get('/questions?page=9999')
        self.assertEqual(res.status_code, 404)

    
    def test_delete_nonexistent_question(self):
        res = self.client.delete('/questions/9999')
        self.assertEqual(res.status_code, 404)

    def test_delete_question_success(self):
        with self.app.app_context():
            q = Question(
                question="Temp",
                answer="Temp",
                difficulty=1,
                category=str(self.category_id)
            )
            q.insert()
            q_id = q.id

        res = self.client.delete(f'/questions/{q_id}')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    
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

    def test_create_question_failure(self):
        res = self.client.post('/questions', json={
            "question": "Incomplete"
        })

        self.assertEqual(res.status_code, 400)

    
    def test_search_questions(self):
        res = self.client.post('/questions', json={
            "searchTerm": "Test"
        })
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIn('totalQuestions', data)

    def test_search_questions_failure(self):
        res = self.client.post('/questions', json={
            "searchTerm": "xyz_not_found"
        })
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)

    
    def test_get_questions_by_category(self):
        res = self.client.get(f'/categories/{self.category_id}/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_questions_by_category_failure(self):
        res = self.client.get('/categories/9999/questions')
        self.assertEqual(res.status_code, 404)

    
    def test_play_quiz(self):
        res = self.client.post('/quizzes', json={
            "previous_questions": [],
            "quiz_category": {"id": 0}
        })
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_quiz_failure(self):
        res = self.client.post('/quizzes', json={
            "previous_questions": [],
            "quiz_category": {"id": 9999}
        })
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


if __name__ == "__main__":
    unittest.main()