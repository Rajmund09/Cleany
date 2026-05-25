import pandas as pd
import numpy as np

def generate_summary(df):
    """
    Generates summary statistics for a dataframe.
    """
    summary = {}
    
    # General info
    summary['total_rows'] = len(df)
    summary['total_columns'] = len(df.columns)
    summary['memory_usage'] = df.memory_usage(deep=True).sum() / (1024 * 1024) # MB
    
    # Missing values
    missing_counts = df.isnull().sum()
    summary['total_missing'] = int(missing_counts.sum())
    summary['missing_by_column'] = missing_counts[missing_counts > 0].to_dict()
    
    # Duplicate rows
    summary['duplicate_rows'] = int(df.duplicated().sum())
    
    # Column details
    col_details = []
    for col in df.columns:
        col_type = str(df[col].dtype)
        unique_count = df[col].nunique()
        missing_count = df[col].isnull().sum()
        
        detail = {
            'name': col,
            'type': col_type,
            'unique_count': int(unique_count),
            'missing_count': int(missing_count),
            'missing_percent': round((missing_count / len(df)) * 100, 2) if len(df) > 0 else 0
        }
        
        if pd.api.types.is_numeric_dtype(df[col]):
            desc = df[col].describe()
            detail.update({
                'min': float(desc.get('min', 0)),
                'max': float(desc.get('max', 0)),
                'mean': float(desc.get('mean', 0)),
                'median': float(df[col].median() if not df[col].isnull().all() else 0),
                'std': float(desc.get('std', 0))
            })
            
        col_details.append(detail)
        
    summary['columns'] = col_details
    return summary
