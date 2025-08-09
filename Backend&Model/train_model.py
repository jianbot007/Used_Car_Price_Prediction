import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib

# 1. Load data
df = pd.read_csv('vehicles.csv')

# 2. Initial exploration (optional, remove in final code)
print(f"Initial dataset shape: {df.shape}")
print(df.head())

# 3. Drop columns unlikely useful for price prediction
drop_cols = [
    'id', 'url', 'region_url', 'VIN', 'image_url', 'description',
    'posting_date', 'lat', 'long', 'county', 'state'
]
df = df.drop(columns=drop_cols, errors='ignore')

# 4. Remove rows with missing or zero price
df = df[df['price'].notnull()]
df = df[df['price'] > 0]

# 5. Check for missing values
print("Missing values per column:")
print(df.isnull().sum())

# 6. Select features and target
# Target = price
# Features (example subset, add or remove based on your dataset and relevance)
features = [
    'year', 'manufacturer', 'model', 'condition', 'cylinders', 'fuel',
    'odometer', 'title_status', 'transmission', 'drive', 'size', 'type', 'paint_color'
]

# Keep only features present in df
features = [f for f in features if f in df.columns]

X = df[features]
y = df['price']

# 7. Handle missing values and categorical data
# Separate numeric and categorical features
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features = X.select_dtypes(include=['object']).columns.tolist()

print(f"Numeric features: {numeric_features}")
print(f"Categorical features: {categorical_features}")

# 8. Create transformers for pipeline

# Numeric pipeline: fill missing with median
numeric_transformer = SimpleImputer(strategy='median')

# Categorical pipeline: fill missing with 'missing', then one-hot encode
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# 9. Combine preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# 10. Create full pipeline with model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# 11. Split dataset for training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42)

# 12. Train model
print("Training model...")
model.fit(X_train, y_train)

# 13. Evaluate model
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f"Train R^2 score: {train_score:.3f}")
print(f"Test R^2 score: {test_score:.3f}")

# 14. Save model pipeline to disk
joblib.dump(model, 'car_price_model.pkl')
print("Model saved as 'car_price_model.pkl'")

# Now you can load 'car_price_model.pkl' in your Spring Boot app via Python API or microservice!
