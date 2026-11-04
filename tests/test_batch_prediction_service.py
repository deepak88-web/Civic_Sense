
from backend.app.services.prediction_service import PredictionService


def test_batch_prediction():

    service = PredictionService()

    complaints = [
        "There is a large pothole on the main road.",
        "Garbage has not been collected for several days.",
        "Street lights are not working in our area.",
        "There is a water leakage near my house."
    ]

    results = service.predict_batch(complaints)

    print("\nBatch Prediction Results:\n")

    for result in results:
        print(result)

    assert len(results) == len(complaints)

    for result in results:
        assert result["predicted_category"]

        assert 0 <= result["confidence_score"] <= 1

        assert result["prediction_status"] in [
            "High",
            "Medium",
            "Low"
        ]


if __name__ == "__main__":
    test_batch_prediction()
