
import argparse
import sys

from civicsense.logger import get_logger

from civicsense.pipeline.training_pipeline import TrainingPipeline
from civicsense.pipeline.prediction_pipeline import PredictionPipeline


logger = get_logger(__name__)


def main():

    parser = argparse.ArgumentParser(
        description="CivicSense - Multilingual Civic Complaint Classification"
    )

    parser.add_argument(
        "--mode",
        type=str,
        required=True,
        choices=["train", "predict"],
        help="Choose whether to train the model or predict complaints."
    )

    args = parser.parse_args()

    try:

        if args.mode == "train":

            logger.info("Starting CivicSense training workflow.")

            training_pipeline = TrainingPipeline()

            evaluation_artifact = (
                training_pipeline.initiate_training_pipeline()
            )

            print("\nTraining completed successfully!")
            print(
                "Evaluation metrics:",
                evaluation_artifact.metrics_file_path
            )

        elif args.mode == "predict":

            logger.info("Starting CivicSense prediction workflow.")

            prediction_pipeline = PredictionPipeline()

            prediction_artifact = (
                prediction_pipeline.initiate_prediction_pipeline()
            )

            print("\nPrediction completed successfully!")

            print(
                "Total predictions:",
                prediction_artifact.total_predictions
            )

            print(
                "Low-confidence complaints:",
                prediction_artifact.low_confidence_count
            )

            print(
                "Predictions saved at:",
                prediction_artifact.predictions_file_path
            )

        logger.info("CivicSense execution completed successfully.")

    except Exception:

        logger.exception("CivicSense execution failed.")

        print("\nCivicSense execution failed.")
        print("Check logs/civicsense.log for details.")

        sys.exit(1)


if __name__ == "__main__":
    main()
