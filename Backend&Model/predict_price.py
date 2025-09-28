import pandas as pd
import joblib
import numpy as np

# ---------------------
# 1. Load Model and Encoders
# ---------------------
model = joblib.load("car_price_model_finetuned.pkl")
le_dict = joblib.load("label_encoders.pkl")

# ---------------------
# 2. Define a function to preprocess new data
# ---------------------
def preprocess_input(data: pd.DataFrame):
    # Fill numeric missing with median
    if 'year' in data.columns:
        data['year'] = data['year'].fillna(data['year'].median())
    if 'odometer' in data.columns:
        data['odometer'] = data['odometer'].fillna(data['odometer'].median())

    # Fill categorical missing and apply label encoding
    for col, le in le_dict.items():
        if col in data.columns:
            data[col] = data[col].fillna('missing')
            # Handle unseen labels
            data[col] = data[col].apply(lambda x: x if x in le.classes_ else 'missing')
            # Refit encoder to include 'missing' if not in classes
            if 'missing' not in le.classes_:
                le.classes_ = np.append(le.classes_, 'missing')
            data[col] = le.transform(data[col])
    
    return data

# ---------------------
# 3. Example new input data (you can replace this with any input)
# ---------------------
new_data = pd.DataFrame([{
    "year": 2015,
    "odometer": 60000,
    "manufacturer": "toyota",
    "model": "corolla",
    "condition": "Excellent",
    "cylinders": "4 cylinders",
    "fuel": "gas",
    "title_status": "clean",
    "transmission": "automatic",
    "drive": "fwd",
    "size": "mid-size",
    "type": "sedan",
    "paint_color": "white"
}])

# ---------------------
# 4. Preprocess & Predict
# ---------------------
X_new = preprocess_input(new_data)
predicted_price = model.predict(X_new)[0]

print(f"Predicted Price: ${predicted_price:,.2f}")
