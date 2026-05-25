import pandas as pd

def format_columns(df):
    """
    Standardizes text and numeric formats.
    """
    df_clean = df.copy()
    logs = []
    
    for col in df_clean.columns:
        if pd.api.types.is_string_dtype(df_clean[col]):
            # Strip whitespace
            df_clean[col] = df_clean[col].str.strip()
            
            # Check if it looks like currency/numeric with symbols
            # Simple heuristic: starts with $ or has commas, and mostly digits
            if df_clean[col].str.contains(r'^\$?\d{1,3}(,\d{3})*(\.\d+)?$').any():
                try:
                    df_clean[col] = df_clean[col].replace({r'\$': '', r',': ''}, regex=True).astype(float)
                    logs.append(f"Converted currency/formatted string column '{col}' to numeric.")
                    continue
                except:
                    pass
            
            # Try parsing dates if 'date' in column name or looks like date
            if 'date' in col.lower() or df_clean[col].str.match(r'^\d{4}-\d{2}-\d{2}$').any():
                try:
                    df_clean[col] = pd.to_datetime(df_clean[col])
                    logs.append(f"Parsed column '{col}' as datetime.")
                except:
                    pass
                    
    return df_clean, logs
