# Sustainable-Concrete-Mix-Design-Using-Machine-Learning-and-Optimization
Sustainable Concrete Mix Design Using Machine Learning and Optimization


## 📌 Project Overview
This project presents a machine learning–based system for predicting concrete compressive strength and generating sustainable concrete mix proportions. The system balances structural performance with environmental impact by minimizing CO₂ emissions through optimized use of fly ash and slag as cement replacements.

---

##  Objectives
- Predict concrete compressive strength using machine learning regression models  
- Generate inverse mix designs based on a user-defined target strength (MPa)  
- Optimize material proportions to reduce CO₂ emissions  
- Promote sustainable construction using supplementary cementitious materials  
- Provide a user-friendly desktop interface for practical use  

---

## 📊 Dataset Description

### Original Dataset
The original dataset contains concrete mix compositions and corresponding compressive strength values obtained from standard experimental studies.

### Synthetic Dataset Augmentation
The original dataset was expanded using synthetic data generation techniques to improve model generalization and robustness.

- Statistical resampling and controlled random perturbations were applied  
- Feature distributions and physical constraints were preserved  
- Unrealistic or infeasible mix combinations were avoided  
- The final dataset consists of **10,000 samples**, including original and synthetic data  

> Synthetic data augmentation was performed using statistical sampling techniques to enhance dataset size and diversity while preserving original feature distributions.

---

##  Models Used
The following regression models were trained and evaluated:

- Random Forest Regressor  
- Gradient Boosting Regressor  
- XGBoost  
- LightGBM  
- Support Vector Regressor (SVR)  
- K-Nearest Neighbors (KNN)  

The best-performing model was selected based on R², RMSE, MAE, and MAPE.

---

##  Optimization Approach
An NSGA-II inspired constrained optimization strategy is used to:
- Maintain the target compressive strength  
- Reduce CO₂ emissions  
- Enforce realistic material constraints on cement, slag, fly ash, and curing age  

The output mix is classified as LOW / MODERATE / HIGH CO₂ risk.

---

##  CO₂ Emission Assessment
CO₂ emissions are calculated using standard emission factors for:
- Cement  
- Slag  
- Fly ash  
- Aggregates  
- Water and admixtures  

This enables sustainability-driven decision-making in concrete mix design.

---

##  User Interface
- Built using Tkinter (desktop-based, VS Code compatible)  
- Accepts target compressive strength (MPa) as input  
- Outputs:
  - Achieved compressive strength  
  - Optimized mix proportions  
  - Total CO₂ emission  
  - CO₂ risk level  

---

##  Tech Stack
- Python  
- Scikit-learn  
- XGBoost  
- LightGBM  
- Pandas, NumPy  
- Tkinter  
- Joblib  

---

