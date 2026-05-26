import pandas as pd


def load_data(path):
    """
    Load insurance dataset safely.
    """
    try:
        df = pd.read_csv(path, sep="|")
        return df
    except FileNotFoundError:
        print("Dataset file not found.")
    except Exception as e:
        print(f"Error loading dataset: {e}")
