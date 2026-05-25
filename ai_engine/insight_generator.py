import pandas as pd
from analytics.summary_stats import generate_summary

def generate_insights(df):
    """
    Simulates an AI engine generating natural language insights based on data stats.
    """
    stats = generate_summary(df)
    insights = []
    
    # Missing values insight
    if stats['total_missing'] > 0:
        pct_missing = round((stats['total_missing'] / (stats['total_rows'] * stats['total_columns'])) * 100, 1)
        insights.append({
            'type': 'warning',
            'title': 'Missing Data Detected',
            'message': f"The dataset contains {stats['total_missing']} missing values across {len(stats['missing_by_column'])} columns, affecting roughly {pct_missing}% of the total cells."
        })
    else:
        insights.append({
            'type': 'success',
            'title': 'Complete Data',
            'message': "No missing values were detected. The dataset is structurally complete."
        })
        
    # Duplicates insight
    if stats['duplicate_rows'] > 0:
        insights.append({
            'type': 'warning',
            'title': 'Duplicate Records',
            'message': f"Found {stats['duplicate_rows']} duplicate rows. Consider running the duplication cleaner to ensure record uniqueness."
        })
        
    # Column specific insights (Outliers, high variance)
    for col in stats['columns']:
        if col['type'] in ['int64', 'float64']:
            if col['std'] > (abs(col['mean']) * 2) and col['mean'] != 0:
                insights.append({
                    'type': 'info',
                    'title': f"High Variance in '{col['name']}'",
                    'message': f"The column '{col['name']}' exhibits high variance (Standard Deviation: {col['std']:.2f}). This may indicate the presence of outliers or a wide distribution."
                })
        
        if col['missing_percent'] > 20:
            insights.append({
                'type': 'danger',
                'title': f"Critical Missing Values in '{col['name']}'",
                'message': f"'{col['name']}' is missing {col['missing_percent']}% of its values. Consider dropping this column or applying a robust imputation strategy."
            })
            
    if not insights:
        insights.append({
            'type': 'info',
            'title': 'Dataset Looks Good',
            'message': "The dataset has a clean structure with minimal formatting issues."
        })
        
    return insights
