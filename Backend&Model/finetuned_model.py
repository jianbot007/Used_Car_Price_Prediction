# -------------------------------
# Fine-tuned Car Price Prediction
# -------------------------------

# 1️⃣ Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import lightgbm as lgb
import joblib

# -------------------------------
# 2️⃣ Load CSV (safe for Colab)
# -------------------------------
file_path = "/content/vehicles.csv"  # Colab file path

df = pd.read_csv(
    file_path,
    engine='python',      # messy CSV handle
    on_bad_lines='skip'   # broken/unclosed lines skip
)

print("Initial dataset shape:", df.shape)

# -------------------------------
# 3️⃣ Keep important columns
# -------------------------------
cols_to_keep = ['price', 'year', 'odometer', 'manufacturer', 'model',
                'condition', 'cylinders', 'fuel', 'title_status',
                'transmission', 'drive', 'size', 'type', 'paint_color']

df = df[cols_to_keep]

# -------------------------------
# 4️⃣ Handle missing values
# -------------------------------
df['year'] = df['year'].fillna(df['year'].median())
df['odometer'] = df['odometer'].fillna(df['odometer'].median())

for col in df.select_dtypes('object').columns:
    df[col] = df[col].fillna('missing')

df = df.drop_duplicates()

print("Missing values handled and duplicates removed.")

# -------------------------------
# 5️⃣ Encode categorical
# -------------------------------
cat_cols = df.select_dtypes('object').columns
le_dict = {}

for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    le_dict[col] = le

print("Categorical columns encoded:", list(cat_cols))

# -------------------------------
# 6️⃣ Feature engineering
# -------------------------------
df['car_age'] = 2025 - df['year']
df['odo_per_year'] = df['odometer'] / (df['car_age'] + 1)

# -------------------------------
# 7️⃣ Prepare target and features
# -------------------------------
X = df.drop(['price', 'year', 'odometer'], axis=1)
y = df['price']

# Cap extreme prices
y = np.where(y > 200000, 200000, y)

# Log-transform target
y_log = np.log1p(y)

# -------------------------------
# 8️⃣ Train/test split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_log, test_size=0.2, random_state=42
)

# -------------------------------
# 9️⃣ LightGBM fine-tuned model
# -------------------------------
model = lgb.LGBMRegressor(
    n_estimators=1000,
    learning_rate=0.05,
    num_leaves=50,
    max_depth=10,
    colsample_bytree=0.8,
    subsample=0.8,
    random_state=42,
    n_jobs=-1
)

print("Training model...")
model.fit(X_train, y_train)

# -------------------------------
# 🔟 Prediction & Evaluate
# -------------------------------
y_pred_log = model.predict(X_test)
y_pred = np.expm1(y_pred_log)  # inverse log

rmse = np.sqrt(mean_squared_error(y_test, y_pred_log))  # RMSE in log-space
r2 = r2_score(y_test, y_pred_log)

print(f"RMSE (log-space): {rmse:.2f}")
print(f"R² Score (log-space): {r2:.2f}")

# Optional: view actual vs predicted
df_result = pd.DataFrame({
    'Actual_Price': np.expm1(y_test),
    'Predicted_Price': y_pred
})
print(df_result.head(10))

# -------------------------------
# 1️⃣1️⃣ Save model and encoders
# -------------------------------
joblib.dump(model, "car_price_model_finetuned.pkl")
joblib.dump(le_dict, "label_encoders.pkl")

print("Fine-tuned model and encoders saved successfully.")
