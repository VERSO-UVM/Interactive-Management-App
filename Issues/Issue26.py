'''
Function to store relationship data and weights to seperate csv file- Grace Kinney
'''
import csv

# Initialize empty list to store field names
field_names = []

# Test data to make sure relationship data is stored in csv file correctly
test_Data = {
    'Relationship A-B': 1,
    'Relationship B-A': 2,
    'Relationship B-C': 3,
    'Relationship C-B': 4,
    'Relationship C-A': 5,
    'Relationship A-C': 6
}

# Function to read through and store relationship data in seperate csv file


def storeWeights():

    # Get user input for file name
    file_name = input(
        "Please enter the name you would like to call your file: ")

    # Add csv extension to selected file name
    file_name += ".csv"

    # Test print to console
    print("File name:", file_name)

    # Creating new csv file
    with open(file_name, 'w', newline='') as csvfile:

        # For loop to iterate through relationship data to collect list of field names
        for key in test_Data.keys():
            field_names.append(key)

        # test print to console make sure field names are correctly entered in variable
        print("Field names:", field_names)

        # Create csv writer object, passes csv file object and list of field names
        writer = csv.DictWriter(csvfile, fieldnames=field_names)

        # Write header to csv file (field names)
        writer.writeheader()

        # Write data to csv file (weights)
        writer.writerow(test_Data)

# Testing


def main():
    storeWeights()


if __name__ == '__main__':
    main()
