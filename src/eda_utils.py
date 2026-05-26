def calculate_loss_ratio(df):
    """
    Calculate overall insurance loss ratio.
    """
    return df["TotalClaims"].sum() / df["TotalPremium"].sum()


def calculate_margin(df):
    """
    Calculate policy margins.
    """
    return df["TotalPremium"] - df["TotalClaims"]
