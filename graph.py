import networkx as nx
from networkx.readwrite import json_graph
from models import db_session, Character, Relationship


def make_graph():
    graph = nx.DiGraph()

    session = db_session()

    characters = session.query(Character).all()

    for character in characters:
        graph.add_node(character.name)

    return json_graph.node_link_data(graph)