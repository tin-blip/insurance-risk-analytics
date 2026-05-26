import pandas as pd
import numpy as np
import scipy.stats as stats

def calculate_insurance_kpis(df: pd.DataFrame) -> dict:
    """
    Calculates the three anchor insurance KPIs for a given data segment:
    Claim Frequency, Claim Severity, and Margin.
    """
    total_policies = len(df)
    
    if total_policies == 0:
        return {"claim_frequency": 0.0, "claim_severity": 0.0, "total_margin": 0.0}
    
    # 1. Claim Frequency: Proportion of policies with at least one claim
    policies_with_claims = df[df['TotalClaims'] > 0]
    claim_frequency = len(policies_with_claims) / total_policies
    
    # 2. Claim Severity: Average claim amount given that a claim occurred
    if len(policies_with_claims) > 0:
        claim_severity = policies_with_claims['TotalClaims'].mean()
    else:
        claim_severity = 0.0
        
    # 3. Margin: TotalPremium - TotalClaims 
    total_premium = df['TotalPremium'].sum()
    total_claims = df['TotalClaims'].sum()
    net_margin = total_premium - total_claims
    mean_policy_margin = (df['TotalPremium'] - df['TotalClaims']).mean()

    return {
        "total_policies": total_policies,
        "claim_frequency": claim_frequency,
        "claim_severity": claim_severity,
        "total_segment_margin": net_margin,
        "average_policy_margin": mean_policy_margin
    }

def run_chi2_test(df: pd.DataFrame, group_col: str, group_a: str, group_b: str, target_col: str) -> tuple:
    """
    Runs a Chi-Squared test of independence for categorical outcomes (e.g., Claim vs No Claim).
    Target column must be binary (1 for claim, 0 for no claim).
    """
    # Filter for our two comparison groups
    filtered_df = df[df[group_col].isin([group_a, group_b])]
    
    # Create a contingency table (Cross-tabulation)
    contingency_table = pd.crosstab(filtered_df[group_col], filtered_df[target_col])
    
    # Run the Chi-Squared test
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    return chi2, p_value

def run_two_sample_ttest(df: pd.DataFrame, group_col: str, group_a: str, group_b: str, target_col: str, filter_zeros: bool = False) -> tuple:
    """
    Runs a Two-Sample Independent t-test for numerical outcomes (e.g., Severity or Margin).
    """
    # Isolate the two groups
    data_a = df[df[group_col] == group_a]
    data_b = df[df[group_col] == group_b]
    
    # If testing Severity, we must filter to look ONLY at records where claims occurred (> 0)
    if filter_zeros:
        values_a = data_a[data_a[target_col] > 0][target_col]
        values_b = data_b[data_b[target_col] > 0][target_col]
    else:
        values_a = data_a[target_col]
        values_b = data_b[target_col]
        
    # Run independent t-test (equal_var=False handles groups with different sample sizes/variances safely)
    t_stat, p_value = stats.ttest_ind(values_a, values_b, equal_var=False)
    
    return t_stat, p_value