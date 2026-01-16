# =========================================================
# TRAIN MULTIPLE ML MODELS FOR CONCRETE STRENGTH PREDICTION
# =========================================================

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    VotingRegressor
)

from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

# =========================================================
# 1. LOAD DATASET
# =========================================================

df = pd.read_csv("data/Concrete_Data_10000.csv")

target_col = [c for c in df.columns if "compressive" in c.lower()][0]

X = df.drop(target_col, axis=1)
y = df[target_col]

# =========================================================
# 2. TRAIN-TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================================================
# 3. DEFINE BASE MODELS
# =========================================================

rf = RandomForestRegressor(n_estimators=200, random_state=42)
gb = GradientBoostingRegressor(n_estimators=200, random_state=42)
xgb = XGBRegressor(objective="reg:squarederror", random_state=42)
lgbm = LGBMRegressor(random_state=42)
svr = SVR(C=100)
knn = KNeighborsRegressor(n_neighbors=7)

# =========================================================
# 4. ENSEMBLE MODEL (VOTING REGRESSOR)
# =========================================================

voting = VotingRegressor(
    estimators=[
        ("rf", rf),
        ("gb", gb),
        ("xgb", xgb),
        ("lgbm", lgbm)
    ]
)

# =========================================================
# 5. MODEL DICTIONARY
# =========================================================

models = {
    "Random Forest": rf,
    "Gradient Boosting": gb,
    "XGBoost": xgb,
    "LightGBM": lgbm,
    "SVR": svr,
    "KNN": knn,
    "Voting Ensemble": voting
}

# =========================================================
# 6. TRAIN & EVALUATE
# =========================================================

best_model = None
best_model_name = None
best_r2 = -1

print("\nMODEL PERFORMANCE (R² SCORE)\n")

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    print(f"{name:20s} : {r2:.4f}")

    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        best_model_name = name

# =========================================================
# 7. SAVE BEST MODEL
# =========================================================

joblib.dump(best_model, "best_model.pkl")
joblib.dump(best_model_name, "best_model_name.pkl")

print("\n===================================")
print("BEST MODEL SELECTED :", best_model_name)
print("BEST R² SCORE       :", best_r2)
print("===================================")

