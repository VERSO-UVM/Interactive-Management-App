import csv
import networkx as nx
from flask import Flask, render_template
from flask_app.database.database_access import FactorTBL, RatingsTBL  git 

app = Flask(__name__)

@app.route('/visualization')
def visualization():
    # Read data from CSV file
    with open('output.csv', 'r') as file:
        reader = csv.DictReader(file)
        factors = []
        ratings = []
        for row in reader:
            factors.append(row['Leading Factor'])
            factors.append(row['Following Factor'])
            ratings.append((row['Leading Factor'], row['Following Factor'], int(row['Weight'])))

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes for factors
    for factor in set(factors):
        G.add_node(factor)

    # Add edges for ratings
    for rating in ratings:
        G.add_edge(rating[0], rating[1], weight=rating[2])

    # Render the visualization HTML template, passing the graph as JSON
    return render_template('results.html', graph_data=nx.json_graph.node_link_data(G))

if __name__ == '__main__':
    app.run(debug=True)
# flake8: noqa