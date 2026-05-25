import os
from flask import Blueprint, jsonify, request, current_app
import pandas as pd
from database.models import DatasetModel
from data_cleaning.preprocessing_pipeline import run_pipeline
from analytics.summary_stats import generate_summary
from analytics.quality_score import calculate_quality_score
from analytics.correlation import compute_correlation_matrix
from ai_engine.insight_generator import generate_insights

analytics_bp = Blueprint('analytics', __name__)

def load_dataset(dataset_id, use_cleaned=False):
    dataset = DatasetModel.get_by_id(dataset_id)
    if not dataset:
        return None, None
        
    folder = current_app.config['CLEANED_FOLDER'] if use_cleaned and dataset['status'] == 'cleaned' else current_app.config['RAW_FOLDER']
    file_path = os.path.join(folder, dataset['filename'])
    
    if not os.path.exists(file_path):
        # Fallback to raw if cleaned not found
        file_path = os.path.join(current_app.config['RAW_FOLDER'], dataset['filename'])
        
    try:
        if dataset['filename'].endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        return df, dataset
    except Exception as e:
        return None, None

@analytics_bp.route('/clean/<int:dataset_id>', methods=['POST'])
def clean_dataset(dataset_id):
    df, dataset = load_dataset(dataset_id)
    if df is None:
        return jsonify({'error': 'Dataset not found or failed to load'}), 404
        
    config = request.json or {}
    
    # Run pipeline
    df_clean, logs = run_pipeline(df, config)
    
    # Save cleaned dataset
    cleaned_path = os.path.join(current_app.config['CLEANED_FOLDER'], dataset['filename'])
    if dataset['filename'].endswith('.csv'):
        df_clean.to_csv(cleaned_path, index=False)
    else:
        df_clean.to_excel(cleaned_path, index=False)
        
    # Log actions
    for log in logs:
        DatasetModel.log_cleaning_action(dataset_id, 'cleaning_step', log)
        
    # Calculate new quality score
    score = calculate_quality_score(df_clean)
    DatasetModel.update_status(dataset_id, 'cleaned', score)
    
    return jsonify({
        'message': 'Dataset cleaned successfully',
        'logs': logs,
        'quality_score': score
    })

@analytics_bp.route('/summary/<int:dataset_id>', methods=['GET'])
def get_summary(dataset_id):
    use_cleaned = request.args.get('use_cleaned', 'true').lower() == 'true'
    df, dataset = load_dataset(dataset_id, use_cleaned)
    
    if df is None:
        return jsonify({'error': 'Dataset not found'}), 404
        
    summary = generate_summary(df)
    score = calculate_quality_score(df)
    correlations = compute_correlation_matrix(df)
    insights = generate_insights(df)
    
    return jsonify({
        'summary': summary,
        'quality_score': score,
        'correlations': correlations,
        'insights': insights,
        'status': dataset['status']
    })
    
@analytics_bp.route('/datasets', methods=['GET'])
def list_datasets():
    datasets = DatasetModel.get_all()
    return jsonify({'datasets': datasets})
