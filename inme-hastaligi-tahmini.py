# ---------- Import Libraries ----------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from imblearn.over_sampling import SMOTE

import warnings
warnings.filterwarnings("ignore")

# ---------- Import Data and Perform EDA ----------

df = pd.read_csv("healthcare-dataset-stroke-data.csv")
df = df.drop(["id"], axis=1)

df.info()

describe = df.describe()

plt.figure()
sns.countplot(x="stroke", data=df)
plt.title("İnme Sınıfının Dağılımı")
plt.show()

# ---------- Missing Value (DecisionTreeRegressor) ----------

df.isnull().sum()

DT_bmi_pipe = Pipeline(steps=[
    ("scale", StandardScaler()),  
    ("dtr", DecisionTreeRegressor())  
])

X = df[["gender", "age", "bmi"]].copy()

X.gender = X.gender.replace({"Male": 0, "Female": 1, "Other": -1}).astype(np.uint8)

missing = X[X.bmi.isna()]

X = X[~X.bmi.isna()]
y = X.pop("bmi")

DT_bmi_pipe.fit(X, y)

predicted_bmi = pd.Series(DT_bmi_pipe.predict(missing[["gender", "age"]]), index=missing.index)

df.loc[missing.index, "bmi"] = predicted_bmi

# ---------- Model Prediction ----------

df["gender"] = df["gender"].replace({"Male": 0, "Female": 1, "Other": -1}).astype(np.uint8)
df["Residence_type"] = df["Residence_type"].replace({"Rural": 0, "Urban": 1}).astype(np.uint8)
df["work_type"] = df["work_type"].replace({"Private": 0, "Self-employed": 1, "Govt_job": 2, 
                                           "children": -1, "Never_worked": -2}).astype(np.uint8)

X = df[["gender", "age", "hypertension", "heart_disease", "work_type", "avg_glucose_level", "bmi"]]
y = df["stroke"]

# Apply SMOTE to balance dataset
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.1, random_state=42)

logreg_pipe = Pipeline(steps=[
    ("scale", StandardScaler()), 
    ("LR", LogisticRegression())
])

# Model training
logreg_pipe.fit(X_train, y_train)

# Model testing
y_pred = logreg_pipe.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# ---------- Save the Model ----------

import joblib

joblib.dump(logreg_pipe, "log_reg_model.pkl")  # save the model

loaded_log_reg_pipe = joblib.load("log_reg_model.pkl")  # load the model

# ---------- Testing the Model ----------

new_patient_data = pd.DataFrame({
    "gender": [1],
    "age": [45],
    "hypertension": [1],
    "heart_disease": [0],
    "work_type": [0],
    "avg_glucose_level": [70],
    "bmi": [25]
})

new_patient_data_result = loaded_log_reg_pipe.predict(new_patient_data)

new_patient_data_result_probability = loaded_log_reg_pipe.predict_proba(new_patient_data)










