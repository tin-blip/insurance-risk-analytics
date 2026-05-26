import matplotlib.pyplot as plt


def plot_claim_distribution(df):
    """
    Plot claim distribution histogram.
    """
    df["TotalClaims"].hist(bins=50)

    plt.title("Distribution of Total Claims")
    plt.xlabel("Claims")
    plt.ylabel("Frequency")

    plt.show()
