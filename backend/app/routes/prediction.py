
from fastapi import APIRouter, HTTPException

from backend.app.schemas.complaint_schema import (
    ComplaintRequest,
    ComplaintPredictionResponse
)

from backend.app.services.prediction_service import PredictionService


router = APIRouter(
    prefix="/api/v1",
    tags=["Prediction"]
)

# Create one reusable prediction service instance
prediction_service = PredictionService()


@router.post(
    "/predict",
    response_model=ComplaintPredictionResponse
)
def predict_complaint(request: ComplaintRequest):
    """
    Predict the category of an individual civic complaint.
    """

    try:
        result = prediction_service.predict_complaint(
            request.complaint_text
        )

        return ComplaintPredictionResponse(**result)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=503,
            detail="Prediction model artifacts are unavailable."
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the complaint."
        ) from error
