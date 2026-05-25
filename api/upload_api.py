import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import pandas as pd
from database.models import DatasetModel

upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@upload_bp.route('/file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # To ensure uniqueness, append timestamp or unique ID, but for simplicity we keep original
        file_path = os.path.join(current_app.config['RAW_FOLDER'], filename)
        file.save(file_path)
        
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
                
            dataset_id = DatasetModel.create(
                filename=filename, 
                original_name=file.filename,
                row_count=len(df),
                file_size=os.path.getsize(file_path)
            )
            
            return jsonify({
                'message': 'File uploaded successfully',
                'dataset_id': dataset_id,
                'columns': list(df.columns),
                'row_count': len(df)
            }), 200
        except Exception as e:
            return jsonify({'error': f'Failed to parse file: {str(e)}'}), 500
            
    return jsonify({'error': 'Invalid file format. Please upload a CSV or Excel file.'}), 400

@upload_bp.route('/preview/<int:dataset_id>', methods=['GET'])
def get_preview(dataset_id):
    dataset = DatasetModel.get_by_id(dataset_id)
    if not dataset:
        return jsonify({'error': 'Dataset not found'}), 404
        
    file_path = os.path.join(current_app.config['RAW_FOLDER'], dataset['filename'])
    try:
        if dataset['filename'].endswith('.csv'):
            df = pd.read_csv(file_path, nrows=50) # preview 50 rows
        else:
            df = pd.read_excel(file_path, nrows=50)
            
        # Clean up NaNs for JSON serialization
        df = df.fillna('')
        return jsonify({
            'columns': list(df.columns),
            'data': df.to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
