from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, ForeignKey
from app import db

engine = create_engine('sqlite:///C:\\Users\\isteiner\\Downloads\\CharacterTracker\\database.db', echo=True)

# engine = create_engine('sqlite:///D:\\Files\\Downloads\\CharacterTracker\\database.db', echo=True)

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


class RelationshipType(Base):
    __tablename__ = 'RelationshipType'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), unique=True)

    def __init__(self, description):
        self.description = description


class Relationship(Base):
    __tablename__ = 'Relationship'

    primary = db.Column(db.Integer, ForeignKey('Character.id'), primary_key=True)
    related_to = db.Column(db.Integer, ForeignKey('Character.id'), primary_key=True)
    relationship_type = db.Column(db.Integer, ForeignKey('RelationshipType.id'))

    def __init__(self, primary, related_to, description):
        self.primary = primary
        self.related_to = related_to
        self.relationship_type = description
'''
class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password
'''

# Create tables.
Base.metadata.create_all(bind=engine)
