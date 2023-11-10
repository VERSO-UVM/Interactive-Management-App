'''Python function that takes in file name from user and does error handling'''
import pandas as pd


# @author Fernanda
# @see https://github.com/VERSO-UVM/Interactive-Management-App/issues/17
def csvImport(filename: str) -> pd.DataFrame:

    # Error handeling for opening file
    try:

        # Reads file and turns it into a data frame
        return pd.read_csv(filename)

    # Catches different types of errors
    except FileNotFoundError:
        print("Could not find file.\nMake sure the file name is correct and it is in the same folder as this program")
        return None
    except pd.errors.EmptyDataError:
        print("CSV file is empty.Please try again")
        return None
    except Exception:
        print("An error occured.Please try again")
        return None


def __test():
    csvImport()


if __name__ == '__main__':
    __test()
