import csv
import matplotlib.pyplot as plt
from pandas import DataFrame
import networkx as nx
import sqlite3
from flask_app.database.Alchemy import initialize_database_connection
from flask_app.database.Alchemy import ParticipantTBL, FactorTBL, RatingsTBL, ResultsTBL
from flask_app.lib.dTypes.Participant import Participant
from flask_app.lib.dTypes.Factor import Factor
from flask_app.database.Alchemy import initialize_database_connection
from flask_app.database.database_access import insert_factor, insert_participant, insert_rating, insert_result, fetch, calculate_average_rating    # database connector
__DATABASE_CONNECTION = initialize_database_connection()

example_id_leading = list(fetch(ResultsTBL))[0][0]
example_id_following = list(fetch(ResultsTBL))[0][1]
example_result = list(fetch(ResultsTBL))[0][2]


if __name__ == "__main__":
    # Fetch data from the database
    factors = fetch(FactorTBL)
    ratings = fetch(RatingsTBL)

    # Process fetched data into a dictionary suitable for your diagram creation
    data_dict = {}
    
    
    # Read data from CSV file to dictionary
    data_dict = read_csv_to_dict(e_csv)


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
