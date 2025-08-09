import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error

# ----------------------
# 1. Load model & encoders
# ----------------------
model = joblib.load("car_price_model.pkl")
le_dict = joblib.load("label_encoders.pkl")

# Dataset path
file_path = "vehicles.csv"
df = pd.read_csv(file_path, low_memory=False)

# Columns used for training
cols = ['price', 'year', 'odometer', 'manufacturer', 'model',
        'condition', 'cylinders', 'fuel', 'title_status',
        'transmission', 'drive', 'size', 'type', 'paint_color']

df = df[cols].dropna(subset=['price'])  # Keep only rows with price

# Sample 10k rows for testing
df_sample = df.sample(n=10000, random_state=42)

# Fill numeric missing values
df_sample['year'] = df_sample['year'].fillna(df_sample['year'].median())
df_sample['odometer'] = df_sample['odometer'].fillna(df_sample['odometer'].median())

# Fill categorical missing values
for col in df_sample.select_dtypes('object').columns:
    df_sample[col] = df_sample[col].fillna('missing')

# Encode categorical columns using saved encoders
for col in df_sample.select_dtypes('object').columns:
    le = le_dict[col]
    # Handle unseen labels by mapping unknown to 0
    df_sample[col] = df_sample[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
    df_sample[col] = le.transform(df_sample[col])

# Prepare X and y
X = df_sample.drop('price', axis=1)
y_true = df_sample['price']

# Cap extreme prices to avoid huge errors
y_true = np.where(y_true > 200000, 200000, y_true)

# Predict
y_pred = model.predict(X)

# Metrics
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mae = mean_absolute_error(y_true, y_pred)
mape = np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1))) * 100  # Avoid /0

# Custom accuracy: % of predictions within 30% of actual price
tolerance = 0.3
accuracy = np.mean(np.abs(y_true - y_pred) / np.maximum(y_true, 1) <= tolerance) * 100

print(f"Evaluated on {len(df_sample)} rows")
print(f"RMSE: {rmse:,.2f}")
print(f"MAE: {mae:,.2f}")
print(f"MAPE: {mape:.2f}%")
print(f"Accuracy within 30% tolerance: {accuracy:.2f}%")
