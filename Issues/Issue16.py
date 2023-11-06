'''
Python function that reads in a dataframe and prompts for user input
to organize data based on column names and desired sort.
'''
import pandas as pd

# funtion name to organize data


def organize_Data():
    # read dataframe (using testing csv)
    df = pd.read_csv('test_data/set3.csv')

    # setting pandas to display full length of data in dataframe
    # for user to view
    pd.set_option('display.max_colwidth', None)

    # number of rows of data
    len_of_df = len(df)
    # number of column names
    len_of_Headers = len(list(df.columns))
    # list of column names
    column_Names = list(df.columns)

    # print number of headers and column names
    print("The dataframe has {} column values: {} and {} lines of data.\n".format(
        len_of_Headers, column_Names, len_of_df))

    # user input for sorting
    select_Column = input("Please select a column to sort by:\n")
    select_Order = input(
        "Would you like to view the data in ascending or descending order?(A or D):\n")

    # if the user input for column name is in the dataframe, continue
    if (select_Column in df.columns):
        # if the user input for selected order is ascending
        if select_Order == 'A':
            sorted_asc = df.sort_values(by=select_Column, ascending=True)
            print(sorted_asc)
        # if the user input for selected order is descending
        elif select_Order == 'D':
            sorted_des = df.sort_values(by=select_Column, ascending=False)
            print(sorted_des)
        # if the user input for selected order is incorret
        else:
            print("Invalid sorting order.")
    # if the user input for column name is incorrect
    else:
        print("Invalid column name.")

# testing


def main():
    organize_Data()


if __name__ == '__main__':
    main()
