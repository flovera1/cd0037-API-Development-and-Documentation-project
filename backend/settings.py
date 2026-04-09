import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "trivia.db")
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "trivia_test.db")