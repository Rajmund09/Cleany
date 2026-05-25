import pandas as pd
import os

def export_to_csv(input_path, output_dir):
    filename = os.path.basename(input_path)
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(output_dir, f"{base_name}_cleaned.csv")
    
    if input_path.endswith('.csv'):
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path)
        
    df.to_csv(output_path, index=False)
    return output_path
