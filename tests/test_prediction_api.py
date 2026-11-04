
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.routes.prediction import router


app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_individual_prediction_api():

    response = client.post(
        "/api/v1/predict",
        json={
            "complaint_text": "There is a large pothole on the main road."
        }
    )

    print("\nAPI Response:")
    print(response.json())

    assert response.status_code == 200

    result = response.json()

    assert result["predicted_category"]
    assert 0 <= result["confidence_score"] <= 1

    assert result["prediction_status"] in [
        "High",
        "Medium",
        "Low"
    ]


if __name__ == "__main__":
    test_individual_prediction_api()
