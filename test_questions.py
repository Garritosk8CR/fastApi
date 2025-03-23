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
    assert response.json()["question_text"] == question_data["question_text"]
    assert len(response.json()["choices"]) == len(question_data["choices"])

def test_create_random_question(test_db):
    # Use the test database in the test
    app.dependency_overrides[get_db] = lambda: test_db
    client = TestClient(app)

        # Generate a random question with multiple random choices, 1 correct and the rest incorrect
    num_choices = 4
    question_data = {
        "question_text": "Random question?",
        "choices": [
            {"choice_text": f"Choice {i}", "is_correct": i == 0} for i in range(num_choices)
        ]
    }

    response = client.post("/questions/", json=question_data)
    assert response.status_code == 200
    assert response.json()["question_text"] == question_data["question_text"]
    assert len(response.json()["choices"]) == num_choices
    assert sum(choice["is_correct"] for choice in response.json()["choices"]) == 1