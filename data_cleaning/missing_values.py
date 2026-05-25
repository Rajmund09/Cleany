import pandas as pd
import numpy as np

def handle_missing_values(df, strategy='auto', custom_strategies=None):
    """
    Handles missing values in a dataframe.
    strategy: 'auto' (median for numeric, mode for categorical), 'drop_rows', 'mean', 'median', 'mode'
    custom_strategies: dict of column name -> strategy
    """
    df_clean = df.copy()
    logs = []
    
    missing_before = df.isnull().sum()
    
    if strategy == 'drop_rows':
        before_len = len(df_clean)
        df_clean.dropna(inplace=True)
        after_len = len(df_clean)
        if before_len - after_len > 0:
            logs.append(f"Dropped {before_len - after_len} rows with missing values.")
        return df_clean, logs

    for col in df_clean.columns:
        if df_clean[col].isnull().sum() == 0:
            continue
            
        col_strategy = strategy
        if custom_strategies and col in custom_strategies:
            col_strategy = custom_strategies[col]
            
        if col_strategy == 'auto':
            if pd.api.types.is_numeric_dtype(df_clean[col]):
                col_strategy = 'median'
            else:
                col_strategy = 'mode'
                
        if col_strategy == 'mean':
            val = df_clean[col].mean()
            df_clean[col].fillna(val, inplace=True)
            logs.append(f"Imputed missing values in '{col}' with mean: {val:.2f}")
        elif col_strategy == 'median':
            val = df_clean[col].median()
            df_clean[col].fillna(val, inplace=True)
            logs.append(f"Imputed missing values in '{col}' with median: {val:.2f}")
        elif col_strategy == 'mode':
            val = df_clean[col].mode()[0]
            df_clean[col].fillna(val, inplace=True)
            logs.append(f"Imputed missing values in '{col}' with mode: '{val}'")
        elif str(col_strategy).startswith('constant:'):
            val = col_strategy.split('constant:')[1]
            df_clean[col].fillna(val, inplace=True)
            logs.append(f"Imputed missing values in '{col}' with constant: '{val}'")
            
    return df_clean, logs
