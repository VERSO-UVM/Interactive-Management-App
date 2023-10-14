import pandas as pd

def organize_Data():
    #read dataframe (using testing csv)
    df = pd.read_csv('test_data/set3.csv')

    #setting pandas to display full length of data in dataframe
    #for user to view
    pd.set_option('display.max_colwidth', None)


    #number of data values
    len_of_df = len(df)
    #create number of headers
    len_of_Headers = len(list(df.columns))
    #create list of column names
    column_Names = list(df.columns)

    #print number of headers and column names
    print("The dataframe has {} column values: {} and {} lines of data.\n".format(len_of_Headers, column_Names, len_of_df))

    select_Column = input("Please select a column to sort by:\n")
    select_Order = input("Would you like to view the data in ascending or descending order?(A or D):\n")


    if(select_Column in df.columns):
        if select_Order == 'A':
            sorted_asc = df.sort_values(by=select_Column, ascending=True)
            print(sorted_asc)
        elif select_Order == 'D':
            sorted_des = df.sort_values(by=select_Column, ascending=False)
            print(sorted_des)
        else:
            print("Invalid sorting order.")
    else:
        print("Invalid column name.")

def main():
    organize_Data()

if __name__ == '__main__':
    main()