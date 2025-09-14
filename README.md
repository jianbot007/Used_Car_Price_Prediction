# Used Car Price Prediction

A Machine Learning project demonstrating how to build, deploy, and serve a used car price prediction model with a Python FastAPI backend and a React/Next.js frontend. This repository guides you through model training, API development with CORS support, and building a user-friendly web interface for real-time price estimation.

## Features

- **Machine Learning Model**: Predicts used car prices based on relevant features.
- **Backend**: Built with Python and FastAPI for robust, scalable API development.
- **Frontend**: Interactive web app using React and Next.js for seamless user experiences.
- **CORS Support**: Backend is configured for secure cross-origin requests from the frontend.
- **End-to-End Pipeline**: From data preprocessing and model training to deployment and serving predictions through an API.

## Project Structure

```
.
├── backend/          # FastAPI backend for ML inference
├── frontend/         # React/Next.js frontend
├── data/             # Datasets for training and testing
├── models/           # Saved ML models
├── requirements.txt  # Python dependencies
├── package.json      # Frontend dependencies
└── ...
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js & npm

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Accessing the Application

- The FastAPI backend will run on `http://localhost:8000`
- The React frontend will run on `http://localhost:3000`

## Usage

1. Start the backend and frontend servers.
2. Open the frontend in your browser.
3. Enter car details into the provided form.
4. Get instant price predictions powered by the ML model.

## Model Training

The project includes Jupyter notebooks/scripts for preprocessing data, training, and evaluating machine learning models for car price prediction. Trained models are saved in the `models/` directory and loaded by the FastAPI backend.

## API Endpoints

- `POST /predict`: Receives car features as input and returns the predicted price.

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests for improvements or bug fixes.

## License

This project is open source. See the repository for licensing details.

---

**Author:** [jianbot007](https://github.com/jianbot007)  
**Repository:** [Used_Car_Price_Prediction](https://github.com/jianbot007/Used_Car_Price_Prediction)
