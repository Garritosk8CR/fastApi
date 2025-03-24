import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from database import engine, SessionLocal
from models import Base, Question, Choices

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

def test_create_questions(test_db):
    # Use the test database in the test
    app.dependency_overrides[get_db] = lambda: test_db
    client = TestClient(app)
    question_data = {
        "question_text": "What is the capital of France?",
        "choices": [
            {"choice_text": "Paris", "is_correct": True},
            {"choice_text": "London", "is_correct": False},
            {"choice_text": "Berlin", "is_correct": False}
        ]
    }
    response = client.post("/questions/", json=question_data)
    assert response.status_code == 200

def test_create_random_question(test_db):
    # Use the test database in the test
    app.dependency_overrides[get_db] = lambda: test_db
    client = TestClient(app)

    num_choices = 4
    question_data = {
        "question_text": "Random question?",
        "choices": [
            {"choice_text": f"Choice {i}", "is_correct": i == 0} for i in range(num_choices)
        ]
    }

    response = client.post("/questions/", json=question_data)
    response.raise_for_status()
    assert response.status_code == 200

def test_read_question_not_found(test_db):
    # Use the test database in the test
    app.dependency_overrides[get_db] = lambda: test_db
    client = TestClient(app)

    # Create a question in the database
    db_question = Question(question_text="Test question")
    test_db.add(db_question)
    test_db.commit()

    response = client.get(f"/questions/{db_question.id + 1}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Question not found"

def test_read_question_found(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    client = TestClient(app)

    db_question = Question(question_text="Test question")
    test_db.add(db_question)
    test_db.commit()

    response = client.get(f"/questions/{db_question.id}")
    assert response.status_code == 200