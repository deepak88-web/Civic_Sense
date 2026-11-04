
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class ComplaintRequest(BaseModel):
    """Request schema for individual complaint prediction."""

    model_config = ConfigDict(str_strip_whitespace=True)

    complaint_text: str = Field(
        ...,
        min_length=1,
        description="The civic complaint text submitted by the user."
    )


class ComplaintPredictionResponse(BaseModel):
    """Response schema for individual complaint prediction."""

    complaint_text: str

    predicted_category: str

    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Prediction confidence score between 0 and 1."
    )

    prediction_status: Literal["High", "Medium", "Low"]



class BatchPredictionResponse(BaseModel):
    """Summary of a completed batch prediction."""

    total_complaints: int

    high_confidence_count: int

    medium_confidence_count: int

    low_confidence_count: int

    output_filename: str

    message: str

    download_url: str
