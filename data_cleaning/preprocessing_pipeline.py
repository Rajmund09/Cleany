import pandas as pd
from .missing_values import handle_missing_values
from .duplicate_handler import handle_duplicates
from .formatter import format_columns
from .outlier_detection import handle_outliers

def run_pipeline(df, config=None):
    """
    Runs the full cleaning pipeline based on config.
    config defaults to standard auto-cleaning.
    """
    if config is None:
        config = {
            'remove_duplicates': True,
            'format_columns': True,
            'missing_values': 'auto', # 'auto', 'drop_rows', etc.
            'handle_outliers': 'clip'
        }
        
    df_clean = df.copy()
    all_logs = []
    
    if config.get('remove_duplicates', True):
        df_clean, logs = handle_duplicates(df_clean)
        all_logs.extend(logs)
        
    if config.get('format_columns', True):
        df_clean, logs = format_columns(df_clean)
        all_logs.extend(logs)
        
    if config.get('missing_values'):
        strategy = config['missing_values']
        df_clean, logs = handle_missing_values(df_clean, strategy=strategy)
        all_logs.extend(logs)
        
    if config.get('handle_outliers'):
        action = config['handle_outliers']
        df_clean, logs = handle_outliers(df_clean, action=action)
        all_logs.extend(logs)
        
    if not all_logs:
        all_logs.append("No cleaning actions were necessary. Data is clean.")
        
    return df_clean, all_logs
