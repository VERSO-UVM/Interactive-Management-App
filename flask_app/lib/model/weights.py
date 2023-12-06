'''
Function to store relationship data and weights to seperate csv file- Grace Kinney
'''
import csv


# @author Grace
# Function to read through and store relationship data in seperate csv file
def storeWeights(file_name: str, data: dict = None):

    field_names = []

    # Creating new csv file
    with open(file_name, 'w', newline='') as csvfile:

        # For loop to iterate through relationship data to collect list of field names
        for key in data.keys():
            field_names.append(key)

        # test print to console make sure field names are correctly entered in variable
        print("Field names:", field_names)

        # Create csv writer object, passes csv file object and list of field names
        writer = csv.DictWriter(csvfile, fieldnames=field_names)

        # Write header to csv file (field names)
        writer.writeheader()

        # Write data to csv file (weights)
        writer.writerow(data)


# Test data to make sure relationship data is stored in csv file correctly
def __test():

    # Initialize empty list to store field names
    test_Data = {
        'Relationship A-B': 1,
        'Relationship B-A': 2,
        'Relationship B-C': 3,
        'Relationship C-B': 4,
        'Relationship C-A': 5,
        'Relationship A-C': 6
    }
    storeWeights(file_name="../../app-tests/test-data/set1.csv",
                 data=test_Data)


if __name__ == '__main__':
    __test()
