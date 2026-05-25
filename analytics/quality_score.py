import pandas as pd

def calculate_quality_score(df):
    """
    Calculates a data quality score out of 100 based on missing values, duplicates, and cardinality.
    """
    if len(df) == 0:
        return 0
        
    total_cells = len(df) * len(df.columns)
    missing_cells = df.isnull().sum().sum()
    missing_penalty = (missing_cells / total_cells) * 40 # Max 40 points penalty
    
    duplicate_rows = df.duplicated().sum()
    duplicate_penalty = (duplicate_rows / len(df)) * 30 # Max 30 points penalty
    
    # Data type consistency / cardinality (rough proxy: high cardinality text might be messy)
    # Let's keep it simple: 100 - penalties
    
    score = 100 - missing_penalty - duplicate_penalty
    return max(0.0, min(100.0, round(score, 1)))
