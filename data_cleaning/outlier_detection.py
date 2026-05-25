import pandas as pd
import numpy as np

def handle_outliers(df, method='iqr', action='clip', columns=None):
    """
    method: 'iqr' or 'zscore'
    action: 'clip' (cap at boundaries) or 'drop'
    """
    df_clean = df.copy()
    logs = []
    
    if columns is None:
        columns = df_clean.select_dtypes(include=[np.number]).columns
        
    outliers_handled = 0
    
    for col in columns:
        if not pd.api.types.is_numeric_dtype(df_clean[col]):
            continue
            
        if method == 'iqr':
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
        else: # zscore
            mean = df_clean[col].mean()
            std = df_clean[col].std()
            lower_bound = mean - 3 * std
            upper_bound = mean + 3 * std
            
        mask = (df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)
        count = mask.sum()
        
        if count > 0:
            outliers_handled += count
            if action == 'clip':
                df_clean[col] = np.clip(df_clean[col], lower_bound, upper_bound)
                logs.append(f"Clipped {count} outliers in '{col}' to bounds [{lower_bound:.2f}, {upper_bound:.2f}].")
            elif action == 'drop':
                df_clean = df_clean[~mask]
                logs.append(f"Dropped {count} rows due to outliers in '{col}'.")
                
    return df_clean, logs
