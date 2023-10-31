'''Function to store relationship data and weights to seperate csv file'''
import csv

# Initialize empty list to store field names
field_names = []

# Test data to make sure relationship data is stored in csv file correctly
test_Data = {
    'Relationship A-B' : 1,
    'Relationship B-A' : 2,
    'Relationship B-C' : 3,
    'Relationship C-B' : 4,
    'Relationship C-A' : 5,
    'Relationship A-C' : 6
}

# Function to read through relationship data and 
def storeWeights():

    with open(file_name, 'w', newline='') as csvfile:
        # Get user input for file name
        file_name = input("Please enter the name you would like to call your file: ")

        # Add csv extension to selected file name
        file_name += ".csv"

        # For loop to iterate through relationship data to collect list of field names
        for key in test_Data:
            field_names.append(key)

        # Create csv writer object, passes csv file object and list of field names
        writer = csv.DictWriter(csvfile, field_names = field_names)

        # Write header to csv file
        writer.writeheader()

        # Write data to csv file
        writer.writerow(test_Data)