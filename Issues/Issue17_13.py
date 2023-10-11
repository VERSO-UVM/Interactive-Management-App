'''Python function that takes in file name from user and does error handling'''
import pandas as pd

def csvImport():
    keepRunning=True
    while(keepRunning==True):
        #Getting user's input for filename
        fileName=input("Please enter file name:\n")


        #Error handeling for opening file
        try:
            #Reads file and turns it into a data frame
            fileInfo=pd.read_csv(fileName)
            keepRunning=False

        #Catches different types of errors    
        except FileNotFoundError:
            print("Could not find file.\nMake sure the file name is correct and it is in the same folder as this program")
        except pd.errors.EmptyDataError:
            print("CSV file is empty.Please try again")
        except Exception:
            print("An error occured.Please try again")

#Testing purposes            
def main():
    csvImport()

main()