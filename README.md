+# Used Car Price Prediction - End-to-End Machine Learning Project

This project demonstrates an end-to-end workflow of a machine learning application, from data processing and model training to deploying a REST API backend and building a modern frontend UI for predictions.

---

## Features

- **ML Model**: Trains a regression model to predict used car prices based on various features such as year, odometer reading, condition, manufacturer, and more.
- **Backend API**: FastAPI-based REST API serving predictions with proper CORS configuration to communicate seamlessly with the frontend.
- **Frontend UI**: Built with React and Next.js using Tailwind CSS for styling. Users can input car details and get real-time price predictions.
- **Data Encoding**: Handles categorical data encoding with LabelEncoders saved and loaded for consistent preprocessing.
- **Error Handling**: Frontend displays loading state and prediction results or error messages.

---

## Tech Stack

- Python, scikit-learn, pandas, numpy — for ML training and data processing
- FastAPI — lightweight, fast API framework for serving predictions
- Joblib — model and encoder serialization
- React, Next.js — frontend framework with client components
- Tailwind CSS — utility-first styling for UI

---

## Setup and Usage

### Backend

1. Clone the repo and navigate to the backend folder.

2. Install Python dependencies:

```bash
pip install fastapi uvicorn scikit-learn pandas numpy joblib
