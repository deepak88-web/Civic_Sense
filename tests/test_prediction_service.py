
from backend.app.services.prediction_service import PredictionService


def test_individual_complaint_prediction():

    service = PredictionService()

    result = service.predict_complaint(
        "There is a large pothole on the main road."
    )

    print("\nPrediction Result:")
    print(result)

    assert result["predicted_category"]
    assert 0 <= result["confidence_score"] <= 1

    assert result["prediction_status"] in [
        "High",
        "Medium",
        "Low"
    ]


if __name__ == "__main__":
    test_individual_complaint_prediction()
