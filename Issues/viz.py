import csv
import matplotlib.pyplot as plt
from pandas import DataFrame
import networkx as nx

# Function to read data from a CSV file to a dictionary
def read_csv_to_dict(filename):
    data_dict = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_dict[int(row['ID'])] = {
                'Leading Factor': row['Leading Factor'],
                'Following Factor': row['Following Factor'],
                'Weight': int(row['Weight'])
            }
    return data_dict

if __name__ == "__main__":
    # Specify the existing CSV filename
    e_csv = 'output2.csv'
    
    # Read data from CSV file to dictionary
    data_dict = read_csv_to_dict(e_csv)

    # Convert the dictionary to a pandas DataFrame
    df = DataFrame.from_dict(data_dict, orient='index')

    # Add an "ID" column 
    df.insert(0, "ID", df.index)

    # Generate NetworkX graph
    G = nx.DiGraph()  # Use DiGraph for directed graph
    for key, value in data_dict.items():
        leading_factor = value['Leading Factor']
        following_factor = value['Following Factor']
        weight = value['Weight']

        # Add nodes for leading and following factors
        G.add_node(leading_factor, pos=(1, key))
        G.add_node(following_factor, pos=(2, key))

        # Add edge with arrow from leading to following factor, weight as label
        G.add_edge(leading_factor, following_factor, weight=weight, label=weight)

    # Define positions of the nodes
    pos = nx.get_node_attributes(G, 'pos')
    # two subplots: one for the NetworkX graph and one for the table
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  

    # networkX
    # networkX
    nx.draw(G, pos, with_labels=True, font_weight='normal', node_size=2000, font_family='sans-serif', ax=ax1)

    # Increase the size of the nodes and set the font style to normal
    # Increase the size of the nodes and set the font style to normal
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)


    # table
    ax2.axis('off')  
    table = ax2.table(cellText=df.values,
                      colLabels=df.columns,
                      cellLoc='center',
                      loc='center')

    # Save both plots as SVG files
    plt.savefig('networkx_and_table.svg', format='svg', bbox_inches='tight')

    plt.show() 
    # flake8: noqa
