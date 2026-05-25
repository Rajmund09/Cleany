import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from database.models import DatasetModel
from analytics.summary_stats import generate_summary
from ai_engine.insight_generator import generate_insights

def export_to_pdf(input_path, output_dir, dataset_id):
    filename = os.path.basename(input_path)
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(output_dir, f"{base_name}_report.pdf")
    
    if input_path.endswith('.csv'):
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path)
        
    dataset = DatasetModel.get_by_id(dataset_id)
    logs = DatasetModel.get_logs(dataset_id)
    stats = generate_summary(df)
    insights = generate_insights(df)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom Styles for CleanFlow AI
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], textColor=colors.HexColor('#2B2B2B'), fontSize=24, spaceAfter=20)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], textColor=colors.HexColor('#6E8793'), fontSize=16, spaceAfter=10)
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], textColor=colors.HexColor('#2B2B2B'), fontSize=11, leading=14)
    
    elements.append(Paragraph(f"CleanFlow AI Data Report", title_style))
    elements.append(Paragraph(f"Dataset: {dataset['original_name']}", normal_style))
    elements.append(Paragraph(f"Status: {dataset['status'].capitalize()}", normal_style))
    if dataset['quality_score']:
        elements.append(Paragraph(f"Quality Score: {dataset['quality_score']}/100", normal_style))
    elements.append(Spacer(1, 20))
    
    # Insights Section
    elements.append(Paragraph("AI Insights", heading_style))
    for insight in insights:
        elements.append(Paragraph(f"<b>{insight['title']}:</b> {insight['message']}", normal_style))
        elements.append(Spacer(1, 10))
        
    elements.append(Spacer(1, 20))
    
    # Cleaning Logs
    if logs:
        elements.append(Paragraph("Cleaning Log", heading_style))
        log_data = [["Time", "Action Taken"]]
        for log in logs:
            log_data.append([str(log['created_at']).split('.')[0], log['details']])
            
        t = Table(log_data, colWidths=[120, 350])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#8FB7C9')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F5F3EE')),
            ('GRID', (0,0), (-1,-1), 1, colors.white),
        ]))
        elements.append(t)
        
    doc.build(elements)
    return output_path
