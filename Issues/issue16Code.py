import pandas as pd

#read dataframe (using testing csv)
df = pd.read_csv('../test_data/set3.csv')

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



# sort votes by ascending or descending (most votes vs. fewest votes)

# if there is a dataframe with no votes category, then either print dataset to console
# or send user a message that there is no numerica category, please reference the datasheet




























###prompt to select column name
##select_Column = input("Please select one of the column values to organize the data by:\n")
###prompt to select order of column name
##select_Order = input("Please select to order dataset in ascending or descending (A or D):\n")
##
###organize data based on fcators and ascending order
##if ((select_Column == "factors") and (select_Order == "A")):
##    sorted_df_Asc = df.sort_values(by=["factors"])
##    print(sorted_df_Asc)
###organize data based on factors and descending order
##elif ((select_Column == "factors") and (select_Order == "D")):
##    sorted_df_Des = df.sort_values(by=["factors"], ascending=False)
##    print(sorted_df_Des)
###organize data based on votes and ascending order
##elif ((select_Column == "votes") and (select_Order == "A")):
##    sorted_df_Asc = df.sort_values(by=["votes"])
##    print(sorted_df_Asc)
###organize data based on votes and descending order
##elif ((select_Column == "votes") and (select_Order == "D")):
##    sorted_df_Des = df.sort_values(by=["votes"], ascending=False)
##    print(sorted_df_Des)


#print entire dataframe for user to view
#print("This is the dataset:\n")
#print(df)

#print top 5 lines of dataframe for testing
#print(df.head())

#print bottom 5 lines of dataframe for testing
#print(df.tail())

#print top 15 lines of data for testing
#print(df.head(15))
