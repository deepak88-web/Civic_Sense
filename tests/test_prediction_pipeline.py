
import pandas as pd

from civicsense.pipeline.prediction_pipeline import PredictionPipeline


# Step 1: Initialize prediction pipeline
prediction_pipeline = PredictionPipeline()


# Step 2: Execute complete prediction workflow
prediction_artifact = (
    prediction_pipeline.initiate_prediction_pipeline()
)


# Step 3: Load generated prediction files
predictions = pd.read_csv(
    prediction_artifact.predictions_file_path
)

summary = pd.read_csv(
    prediction_artifact.prediction_summary_file_path
)


# Step 4: Display results
print("\nCOMPLETE PREDICTION PIPELINE RESULTS")
print("------------------------------------")

print("Total predictions:", len(predictions))

print(
    "Low-confidence complaints:",
    prediction_artifact.low_confidence_count
)

print("\nConfidence distribution:")
print(predictions["prediction_status"].value_counts())

print("\nCategory distribution:")
print(predictions["predicted_category"].value_counts())


# Step 5: Verify results
assert len(predictions) == 27686

assert len(predictions) == prediction_artifact.total_predictions

assert predictions["predicted_category"].notna().all()

assert predictions["confidence_score"].between(0, 1).all()

assert set(predictions["prediction_status"].unique()).issubset(
    {"High", "Medium", "Low"}
)

assert len(summary) > 0

assert prediction_artifact.predictions_file_path.exists()

assert prediction_artifact.low_confidence_file_path.exists()

assert prediction_artifact.prediction_summary_file_path.exists()


print("\nPrediction Pipeline Test Successful!")
print("All prediction stages completed.")
