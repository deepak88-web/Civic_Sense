
import os
import uuid
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from backend.app.schemas.complaint_schema import (
    ComplaintRequest,
    ComplaintPredictionResponse,
    BatchPredictionResponse
)
from backend.app.services.prediction_service import PredictionService


router = APIRouter(prefix="/api/v1", tags=["Prediction"])

prediction_service = PredictionService()

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BATCH_OUTPUT_DIR = PROJECT_ROOT / "artifacts" / "api_predictions"


@router.post(
    "/predict",
    response_model=ComplaintPredictionResponse
)
def predict_complaint(request: ComplaintRequest):
    try:
        result = prediction_service.predict_complaint(
            request.complaint_text
        )
        return ComplaintPredictionResponse(**result)

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

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


@router.post(
    "/predict/batch",
    response_model=BatchPredictionResponse
)
def predict_batch(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file."
        )

    try:
        dataframe = pd.read_csv(file.file)

        if dataframe.empty:
            raise HTTPException(
                status_code=400,
                detail="The uploaded CSV file is empty."
            )

        if "complaint_text" not in dataframe.columns:
            raise HTTPException(
                status_code=400,
                detail="The CSV must contain a 'complaint_text' column."
            )

        if dataframe["complaint_text"].isna().any():
            raise HTTPException(
                status_code=400,
                detail="The complaint_text column contains empty values."
            )

        complaint_texts = dataframe["complaint_text"].astype(str).tolist()

        if any(not text.strip() for text in complaint_texts):
            raise HTTPException(
                status_code=400,
                detail="The complaint_text column contains blank values."
            )

        predictions = prediction_service.predict_batch(complaint_texts)

        prediction_dataframe = pd.DataFrame(predictions)

        dataframe["predicted_category"] = prediction_dataframe[
            "predicted_category"
        ]
        dataframe["confidence_score"] = prediction_dataframe[
            "confidence_score"
        ]
        dataframe["prediction_status"] = prediction_dataframe[
            "prediction_status"
        ]

        BATCH_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        output_filename = f"civicsense_predictions_{uuid.uuid4().hex[:8]}.csv"
        output_path = BATCH_OUTPUT_DIR / output_filename

        dataframe.to_csv(output_path, index=False)

        total = len(predictions)
        high_count = sum(
            p["prediction_status"] == "High" for p in predictions
        )
        medium_count = sum(
            p["prediction_status"] == "Medium" for p in predictions
        )
        low_count = sum(
            p["prediction_status"] == "Low" for p in predictions
        )

        return BatchPredictionResponse(
            total_complaints=total,
            high_confidence_count=high_count,
            medium_confidence_count=medium_count,
            low_confidence_count=low_count,
            output_filename=output_filename,
            download_url=f"/api/v1/predict/batch/download/{output_filename}",
            message="Batch prediction completed successfully."
        )

    except HTTPException:
        raise

    except pd.errors.EmptyDataError as error:
        raise HTTPException(
            status_code=400,
            detail="The uploaded CSV file is empty or invalid."
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="An error occurred during batch prediction."
        ) from error

    finally:
        file.file.close()


@router.get(
    "/predict/batch/download/{filename}",
    tags=["Prediction"]
)
def download_batch_predictions(filename: str):

    if not filename.startswith("civicsense_predictions_") or not filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Invalid output filename."
        )

    output_path = BATCH_OUTPUT_DIR / filename

    if not output_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Prediction output file not found."
        )

    return FileResponse(
        path=output_path,
        media_type="text/csv",
        filename=filename
    )
