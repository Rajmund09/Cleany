import pandas as pd
import numpy as np

def compute_correlation_matrix(df, method='pearson'):
    """
    Computes a correlation matrix for numeric columns.
    Returns format suitable for Chart.js or D3.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return None
        
    corr = numeric_df.corr(method=method)
    
    # Convert to a format easily consumed by frontend
    labels = list(corr.columns)
    datasets = []
    
    for i, row_label in enumerate(labels):
        for j, col_label in enumerate(labels):
            val = corr.iloc[i, j]
            if not np.isnan(val):
                datasets.append({
                    'x': col_label,
                    'y': row_label,
                    'v': round(val, 3)
                })
                
    return {
        'labels': labels,
        'data': datasets
    }
