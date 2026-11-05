# CivicSense – Multilingual Civic Complaint Classification

CivicSense is a multilingual civic complaint classification application that uses Natural Language Processing and Deep Learning to automatically categorize civic complaints into relevant categories.

## Live Deployment

- **Frontend:** [CivicSense Website](https://ashy-ground-0498e9000.6.azurestaticapps.net/)
- **Backend Health:** [API Health Check](https://civicsense-api.kindforest-b590cba3.eastasia.azurecontainerapps.io/health)
- **API Documentation:** [FastAPI Swagger UI](https://civicsense-api.kindforest-b590cba3.eastasia.azurecontainerapps.io/docs)

## Project Repositories and Docker Image

- **GitHub Repository:** [CivicSense](https://github.com/deepak88-web/Civic_Sense)
- **Docker Hub:** [CivicSense Backend Image](https://hub.docker.com/r/deepakyad/civicsense-backend)

## Technology Stack

**Frontend**
- React.js
- Vite
- JavaScript
- Axios

**Backend**
- Python
- FastAPI
- Uvicorn

**Machine Learning**
- TensorFlow / Keras
- LSTM
- Word2Vec
- NLP
- Scikit-learn

**Deployment and Infrastructure**
- Docker
- Docker Hub
- Azure Container Apps (Consumption)
- Azure Static Web Apps
- GitHub Actions

## Model and Prediction

CivicSense uses an LSTM-based classification model with Word2Vec embeddings to classify multilingual civic complaints into 12 categories.

The prediction API provides:
- Predicted complaint category
- Confidence score
- Prediction status

## Running Locally

Clone the repository:

```bash
git clone https://github.com/deepak88-web/Civic_Sense.git
cd Civic_Sense
```

Follow the project-specific installation and setup instructions for the backend and frontend.

## Deployment Architecture

- The React frontend is hosted on Azure Static Web Apps.
- The FastAPI backend runs in Azure Container Apps.
- The trained model and required artifacts are packaged inside a Docker image.
- GitHub Actions automates frontend deployment.

## Project Status

Deployed and accessible online.