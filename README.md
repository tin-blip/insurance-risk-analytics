# Insurance Risk Analytics

This project analyzes historical insurance claim data to identify risk patterns, evaluate portfolio profitability, perform hypothesis testing, and build predictive models for dynamic insurance pricing.

## Tasks

- Exploratory Data Analysis (EDA)
- Data Version Control (DVC)
- A/B Hypothesis Testing
- Predictive Modeling

## Technologies

- Python
- Pandas
- Scikit-learn
- XGBoost
- DVC
- GitHub Actions


## Data Version Control (DVC)

This project uses DVC (Data Version Control) to manage and version datasets separately from Git.

### Dataset Tracking

The raw insurance dataset is tracked using DVC rather than storing large data files directly in the Git repository.

### Common DVC Commands

Initialize DVC:

**dvc init**
Track dataset:

**dvc add data/MachineLearningRating_v3.txt**
Push data to remote storage:

**dvc push**
Retrieve tracked datasets:

**dvc pull**

### DVC Remote Storage

A local DVC remote storage directory was configured to ensure reproducibility and proper dataset management across project versions.
