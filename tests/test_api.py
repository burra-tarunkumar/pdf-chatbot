from fastapi.testclient import TestClient
from app.api import app

from unittest.mock import patch

client=TestClient(app)

def test_root():
    response=client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "PDF Chatbot API is running."
    }
def test_empty_test_question():
    response=client.post(
        "/ask",
        json={"question":""})
    assert response.status_code == 422

def test_max_qsn_length():
    question = "a"*1001
    response=client.post(
        "/ask",
        json={"question":question}
    )
    assert response.status_code == 422

def test_ask_question_success():
    fake_result={
        "question":"What is G-DINA?",
        "answer":"G-DINA is a cognitive dignostic model",
        "pages":[4,5]
    }
    with patch("app.api.ask_question",return_value = fake_result):
        response = client.post(
            "/ask",
            json={"question":"What is G-DINA?"}
        )
    assert response.status_code == 200
    assert response.json() == fake_result


def test_ask_question_error():
    with patch(
        "app.api.ask_question",
        side_effect = Exception("Gemini API failed")
    ):
        response = client.post(
            "/ask",
            json={"question":"What is G-DINA?"}
        )
    assert response.status_code == 500
    assert response.json() == {
        "detail":"An error occurred while processing the question"
    }