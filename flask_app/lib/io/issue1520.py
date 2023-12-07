# import pandas
import pandas as pd

#20. Display feedback (success, error) after uploading CSV
def process_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        # This is where we could clean the data. Also where task 15 would go?
        print("CSV uploaded successfully!")
    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
    except Exception as e:
        print("Error: File did not upload correctly.")
     
file_path = 'set1.csv'
process_csv(file_path)

# 15. Check if numeric category exists in the CSV
def numeric(file_path):
    try:
        df2 = pd.read_csv(file_path)
        numeric_cols = df2.select_dtypes(include=['int', 'float']).columns.tolist()
        if numeric_cols:
            print("The dataframe contains the numeric column(s)", numeric_cols)
        else:
            print("No numeric columns")
    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
    except Exception as e:
        print("Error: File did not upload correctly.")        
path = 'set2.csv'
numeric(path)