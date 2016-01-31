from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, ForeignKey
from app import db
import os
import networkx as nx
from networkx.readwrite import json_graph

current_directory = os.path.dirname(__file__)

filename = os.path.join(current_directory, 'database.db')

engine = create_engine('sqlite:///' + filename)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.


class Character(Base):
    __tablename__ = 'Character'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    short_description = db.Column(db.String(256))
    description = db.Column(db.String(10000))

    def __init__(self, name, short_description, description):
        self.name = name
        self.short_description = short_description
        self.description = description

    def get_relationships(self):
        relationships = dict()

        for relationship in db_session().query(Relationship).filter(Relationship.primary == self.id):
            related_to = db_session().query(Character).filter(Character.id == relationship.related_to)
            relationships[related_to] = relationship.description

        return relationships


# class RelationshipType(Base):
#     __tablename__ = 'RelationshipType'
#
#     id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(120), unique=True)
#
#     def __init__(self, description):
#         self.description = description


class Relationship(Base):
    __tablename__ = 'Relationship'

    primary = db.Column(db.Integer, ForeignKey('Character.id'), primary_key=True)
    related_to = db.Column(db.Integer, ForeignKey('Character.id'), primary_key=True)
    relationship_type = db.Column(db.String(100))
    relationship_description = db.Column(db.String(2056))

    def __init__(self, primary, related_to, relationship_type, description):
        self.primary = primary
        self.related_to = related_to
        self.relationship_type = relationship_type
        self.relationship_description = description


def character_count():
    return db_session().query(Character).count()


def relationship_count():
    return db_session().query(Relationship).count()


def make_graph(names):
    graph = nx.DiGraph()

    session = db_session()

    characters = []

    if len(names) > 0:
        characters = session.query(Character).filter(Character.name.in_(names))
    else:
        characters = session.query(Character).all()

    for character in characters:
        relationships = session.query(Relationship).filter(Relationship.primary == character.id)

        # relationship_dict = dict()

        graph.add_node(character.id, {"name": character.name,
                                      "description": character.description,
                                      "short_description": character.short_description
                                      })

        for relationship in relationships:
            graph.add_edge(relationship.primary, relationship.related_to)

            # related_to_name = session.query(Character).get(relationship.related_to).name
            #
            # relationship_dict[related_to_name] = {"relationship_type": relationship.relationship_type,
            #                                               "relationship_description":
            #                                                   relationship.relationship_description}

    return json_graph.node_link_data(graph)

# Create tables.
Base.metadata.create_all(bind=engine)