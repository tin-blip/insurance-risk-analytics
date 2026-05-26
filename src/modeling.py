import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def preprocess_insurance_data(df: pd.DataFrame, target_col: str, task_type: str = 'regression'):
    """
    Cleans, encodes categorical features, and splits the data.
    task_type options: 'regression' (Severity) or 'classification' (Probability).
    """
    data = df.copy()
    
    # 1. Feature Engineering: Calculate Vehicle Age safely
    current_year = 2026
    if 'RegistrationYear' in data.columns:
        data['Vehicle_Age'] = current_year - data['RegistrationYear']
        data['Vehicle_Age'] = data['Vehicle_Age'].fillna(data['Vehicle_Age'].median())
    
    # 2. Select predictive features requested by management
    feature_cols = [
        'Province', 'Gender', 'VehicleType', 'BodyType', 
        'Make', 'Cylinders', 'SumInsured', 'Vehicle_Age'
    ]
    existing_features = [col for col in feature_cols if col in data.columns]
    
    X = data[existing_features].copy()
    
    # 3. Handle Missing Values
    for col in X.columns:
        # Check if the column is numeric (integer or float)
        if pd.api.types.is_numeric_dtype(X[col]):
            X[col] = X[col].fillna(X[col].median())
        else:
            # Fallback for any text, string, or object categorization columns
            fallback_mode = X[col].mode()
            if not fallback_mode.empty:
                X[col] = X[col].fillna(fallback_mode[0])
            else:
                X[col] = X[col].fillna("Unknown")
            
    # 4. Convert Categorical text to numbers (Label Encoding)
    for col in X.columns:
        # Catch both old 'object' types and modern 'string' types
        if X[col].dtype == 'object' or isinstance(X[col].dtype, pd.StringDtype) or X[col].dtype == 'string':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            
    # 5. Handle Track Splits
    if task_type == 'regression':
        # Severity models ONLY look at records where a claim actually happened
        y = data[target_col]
        mask = y > 0
        X = X[mask]
        y = y[mask]
    else:
        # Probability models look at a binary flag: 1 if claim occurred, 0 otherwise
        y = (data[target_col] > 0).astype(int)
        
    # 6. Train-Test Split (80/20 split)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    return X_train, X_test, y_train, y_test