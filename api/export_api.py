import os
from flask import Blueprint, jsonify, send_file, current_app
from database.models import DatasetModel
from exports.csv_export import export_to_csv
from exports.excel_export import export_to_excel
from exports.pdf_export import export_to_pdf

export_bp = Blueprint('export', __name__)

@export_bp.route('/<int:dataset_id>/<format>', methods=['GET'])
def download_export(dataset_id, format):
    dataset = DatasetModel.get_by_id(dataset_id)
    if not dataset:
        return jsonify({'error': 'Dataset not found'}), 404
        
    if dataset['status'] == 'cleaned':
        file_path = os.path.join(current_app.config['CLEANED_FOLDER'], dataset['filename'])
    else:
        file_path = os.path.join(current_app.config['RAW_FOLDER'], dataset['filename'])
        
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
        
    if format == 'csv':
        output_path = export_to_csv(file_path, current_app.config['EXCEL_REPORTS']) # Saving in EXCEL folder as generic reports
        return send_file(output_path, as_attachment=True)
    elif format == 'excel':
        output_path = export_to_excel(file_path, current_app.config['EXCEL_REPORTS'])
        return send_file(output_path, as_attachment=True)
    elif format == 'pdf':
        output_path = export_to_pdf(file_path, current_app.config['PDF_REPORTS'], dataset_id)
        return send_file(output_path, as_attachment=True)
    else:
        return jsonify({'error': 'Invalid format'}), 400
