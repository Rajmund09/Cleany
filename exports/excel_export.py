import pandas as pd
import os

def export_to_excel(input_path, output_dir):
    filename = os.path.basename(input_path)
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(output_dir, f"{base_name}_cleaned.xlsx")
    
    if input_path.endswith('.csv'):
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path)
        
    # Styling can be applied using openpyxl engine
    writer = pd.ExcelWriter(output_path, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Cleaned Data')
    writer.close()
    
    return output_path
