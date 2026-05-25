import os
import pandas as pd
import numpy as np
from config import Config

def create_sample_sales():
    os.makedirs('datasets', exist_ok=True)
    
    np.random.seed(42)
    data = {
        'Order_ID': [f"ORD-{i:04d}" for i in range(1, 101)],
        'Date': pd.date_range(start='2023-01-01', periods=100).strftime('%Y-%m-%d'),
        'Customer_Name': [f"Customer_{np.random.randint(1, 50)}" for _ in range(100)],
        'Revenue': [f"${np.random.randint(100, 5000):,}.00" for _ in range(100)],
        'Quantity': np.random.randint(1, 20, 100)
    }
    
    df = pd.DataFrame(data)
    
    # Introduce duplicates
    df = pd.concat([df, df.iloc[:5]], ignore_index=True)
    
    # Introduce missing values
    df.loc[10:15, 'Customer_Name'] = np.nan
    df.loc[20:25, 'Revenue'] = np.nan
    df.loc[30:35, 'Quantity'] = np.nan
    
    # Introduce outliers
    df.loc[40, 'Quantity'] = 500
    df.loc[41, 'Quantity'] = -50
    
    # Introduce bad formatting
    df.loc[50:55, 'Customer_Name'] = df.loc[50:55, 'Customer_Name'].str.lower() + "  "
    
    df.to_csv('datasets/sample_sales.csv', index=False)
    print("Created datasets/sample_sales.csv")

def create_sample_customers():
    data = {
        'Customer_ID': range(1000, 1050),
        'Name': [f"Person {i}" for i in range(50)],
        'Age': np.random.randint(18, 80, 50),
        'Score': np.random.normal(50, 15, 50)
    }
    df = pd.DataFrame(data)
    
    # Outliers
    df.loc[5, 'Age'] = 150
    df.loc[10, 'Score'] = 1000
    
    # Missing
    df.loc[20:25, 'Score'] = np.nan
    
    df.to_csv('datasets/sample_customers.csv', index=False)
    print("Created datasets/sample_customers.csv")

if __name__ == "__main__":
    create_sample_sales()
    create_sample_customers()
