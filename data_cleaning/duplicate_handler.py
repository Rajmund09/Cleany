import pandas as pd

def handle_duplicates(df, subset=None, keep='first'):
    """
    Removes duplicate rows.
    """
    df_clean = df.copy()
    logs = []
    
    before_len = len(df_clean)
    df_clean.drop_duplicates(subset=subset, keep=keep, inplace=True)
    after_len = len(df_clean)
    
    duplicates_removed = before_len - after_len
    if duplicates_removed > 0:
        logs.append(f"Removed {duplicates_removed} duplicate rows.")
        
    return df_clean, logs
