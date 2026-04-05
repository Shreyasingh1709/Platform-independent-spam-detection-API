# Platform-independent-spam-detection-API

## Overview
This project is a platform-independent spam detection system using a Naive Bayes model and TF-IDF vectorizer. It provides:
- A FastAPI backend for real-time spam/ham prediction and confidence scoring
- A Streamlit dashboard for analytics, trends, and single-message prediction
- MySQL database for storing email messages, predictions, and analytics

## Features
- **Naive Bayes Model**: Trained on email data using TF-IDF features
- **API**: `/predict` endpoint for spam/ham prediction and confidence
- **Dashboard**: Visualizes spam/ham trends, recent emails, and allows manual prediction
- **Preprocessing**: Cleans and normalizes email text before prediction
- **Database**: Stores all predictions and supports analytics

## System Architecture

```mermaid
graph TD
	A[User/Email Client] -->|Send email text| B[API (FastAPI)]
	B -->|Predict spam/ham & confidence| C[Database (MySQL)]
	B -->|Return prediction & confidence| A
	C -->|Data for analytics| D[Dashboard (Streamlit)]
	D -->|Show analytics, trends, predictions| A
	B -->|Uses| E[Naive Bayes Model (model.pkl)]
	B -->|Uses| F[TF-IDF Vectorizer (vectorizer.pkl)]
	B -->|Preprocess| G[Preprocessing (preprocess.py)]
	D -->|Fetches from| C
	D -->|Single message prediction| B
```

## Usage

1. **Train Model**: Run `model_training.py` to train and save `model.pkl` and `vectorizer.pkl`.
2. **Start API**: Run `api.py` (with FastAPI/Uvicorn) to serve predictions.
3. **Dashboard**: Run `dashboard.py` (with Streamlit) to view analytics and predict emails.
4. **Database**: Ensure MySQL is running and accessible as configured in `database.py`.

## File Structure
- `model_training.py`: Trains and saves the Naive Bayes model and vectorizer
- `api.py`: FastAPI backend for predictions
- `dashboard.py`: Streamlit dashboard for analytics and manual predictions
- `database.py`: Database connection and operations
- `preprocess.py`: Text preprocessing functions
- `email_client.py`: Fetches emails for batch prediction
- `model.pkl`, `vectorizer.pkl`: Saved model and vectorizer

## Requirements
- Python 3.10+
- FastAPI, Uvicorn, Streamlit, SQLAlchemy, scikit-learn, pandas, mysql-connector-python

## License
MIT
