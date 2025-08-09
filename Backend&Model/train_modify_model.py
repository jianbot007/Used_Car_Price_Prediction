import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import lightgbm as lgb
import joblib
from sklearn.metrics import root_mean_squared_error

# ---------------------
# 1. Load Dataset
# ---------------------
file_path = "vehicles.csv"  # Change if filename is different
df = pd.read_csv(file_path, low_memory=False)

print("Initial dataset shape:", df.shape)

# Keep only important columns
cols_to_keep = ['price', 'year', 'odometer', 'manufacturer', 'model',
                'condition', 'cylinders', 'fuel', 'title_status',
                'transmission', 'drive', 'size', 'type', 'paint_color']
df = df[cols_to_keep]

# ---------------------
# 2. Handle Missing Values
# ---------------------
# Fill numeric with median
df['year'] = df['year'].fillna(df['year'].median())
df['odometer'] = df['odometer'].fillna(df['odometer'].median())

# Fill categorical with 'missing'
for col in df.select_dtypes('object').columns:
    df[col] = df[col].fillna('missing')

print("Missing values handled.")

# ---------------------
# 3. Encode Categorical Columns
# ---------------------
cat_cols = df.select_dtypes('object').columns
le_dict = {}

for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    le_dict[col] = le

print("Categorical columns encoded:", list(cat_cols))

# ---------------------
# 4. Prepare Data for Model
# ---------------------
X = df.drop('price', axis=1)
y = df['price']

# Optional: remove extreme outliers
y = np.where(y > 200000, 200000, y)  # Cap price at 200k

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------
# 5. Train LightGBM Model
# ---------------------
model = lgb.LGBMRegressor(
    n_estimators=500,
    learning_rate=0.1,
    num_leaves=31,
    max_depth=-1,
    n_jobs=-1,
    random_state=42
)

print("Training model...")
model.fit(X_train, y_train)

# ---------------------
# 6. Evaluate
# ---------------------
y_pred = model.predict(X_test)

rmse = root_mean_squared_error(y_test, y_pred)
print(f"RMSE: {rmse:.2f}")

# ---------------------
# 7. Save Model and Encoders
# ---------------------
joblib.dump(model, "car_price_model.pkl")
joblib.dump(le_dict, "label_encoders.pkl")

print("Model and encoders saved successfully.")
