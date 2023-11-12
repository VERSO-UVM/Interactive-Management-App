"""
csv_importer.py

This Python script defines a function for importing a CSV file using the pandas library. The function takes a filename as input and performs error handling to manage potential issues during the file import process.

@author: Fernanda
@see: https://github.com/VERSO-UVM/Interactive-Management-App/issues/17

Functions:
    csvImport(filename: str) -> pd.DataFrame:
        Takes a filename as input and attempts to read the CSV file using pandas.
        
        Parameters:
            filename (str): The name of the CSV file to be imported.
            
        Returns:
            pd.DataFrame or None: If the file is successfully read, a pandas DataFrame is returned. If an error occurs during the import process, an appropriate error message is printed, and None is returned.

    __test():
        A private test function that calls the csvImport function without any arguments.

Usage:
    To use this script, import the csv_importer module into your Python code and call the csvImport function, providing the desired CSV filename as an argument.

Example:
    import csv_importer
    
    # Example 1: Successful file import
    data_frame = csv_importer.csvImport('example.csv')
    print(data_frame)
    
    # Example 2: Error handling for file not found
    data_frame = csv_importer.csvImport('nonexistent_file.csv')
    if data_frame is None:
        print("Error occurred during file import.")

"""
import pandas as pd


def csvImport(filename: str) -> pd.DataFrame:
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        print("Could not find file.\nMake sure the file name is correct and it is in the same folder as this program")
        return None
    except pd.errors.EmptyDataError:
        print("CSV file is empty. Please try again.")
        return None
    except Exception:
        print("An error occurred. Please try again.")
        return None


def __test():
    """
    A private test function that calls the csvImport function without any arguments.
    """
    csvImport()


if __name__ == '__main__':
    __test()
