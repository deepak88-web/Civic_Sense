
import json

from civicsense.pipeline.training_pipeline import TrainingPipeline


# Step 1: Initialize training pipeline
training_pipeline = TrainingPipeline()


# Step 2: Execute complete training workflow
evaluation_artifact = (
    training_pipeline.initiate_training_pipeline()
)


# Step 3: Display evaluation results
with open(
    evaluation_artifact.metrics_file_path,
    "r",
    encoding="utf-8"
) as file:
    metrics = json.load(file)


print("\nCOMPLETE TRAINING PIPELINE RESULTS")
print("-----------------------------------")

for metric, score in metrics.items():
    print(f"{metric}: {score:.4f}")


# Step 4: Verify generated evaluation artifacts
assert evaluation_artifact.metrics_file_path.exists()

assert (
    evaluation_artifact.classification_report_file_path.exists()
)

assert (
    evaluation_artifact.confusion_matrix_file_path.exists()
)

print("\nTraining Pipeline Test Successful!")
print("All training and evaluation stages completed.")
