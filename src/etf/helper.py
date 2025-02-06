import os
from src.firebase.firebase import load_code
folder_name = 'etf_data'

def save_file(df, file_name):
    output_folder = folder_name
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    csv_file_path = os.path.join(output_folder, file_name)
    df.to_csv(csv_file_path, index=False)
    

def paper_detail():
    return load_code("etf","paper")
    
    