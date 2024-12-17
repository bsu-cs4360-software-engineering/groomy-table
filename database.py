from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.attributes import InstrumentedAttribute

class DatabaseInterface(ABC):
    @abstractmethod
    def init_db(self):
        pass
    
    @property
    @abstractmethod
    def Model(self):
        pass

    @property
    @abstractmethod
    def Column(self):
        pass

    @property
    @abstractmethod
    def Integer(self):
        pass

    @property
    @abstractmethod
    def String(self):
        pass

    @property
    @abstractmethod
    def ForeignKey(self):
        pass

    @property
    @abstractmethod
    def relationship(self):
        pass
    
    @property
    @abstractmethod
    def Numeric(self):
        pass
    
    @property
    @abstractmethod
    def Boolean(self):
        pass
    
    @property
    @abstractmethod
    def Date(self):
        pass
    
    @property
    @abstractmethod
    def Time(self):
        pass

    @property
    @abstractmethod
    def Enum(self):
        pass

    @property
    @abstractmethod
    def Text(self):
        pass

    @property
    @abstractmethod
    def DateTime(self):
        pass

    @property
    @abstractmethod
    def Float(self):
        pass

    @property
    @abstractmethod
    def CheckConstraint(self):
        pass

    @property
    @abstractmethod
    def func(self):
        pass

    @abstractmethod
    def get_session(self):
        pass
    
    @abstractmethod
    def query(self, model):
        pass
    
    @abstractmethod
    def filter_by(self, model, **conditions):
        pass
    
    @abstractmethod
    def joinedload(self, model, *relationships):
        pass
    
    @abstractmethod
    def options(self, *args):
        pass
    
    @abstractmethod
    def order_by(self, *args):
        pass
    
    @abstractmethod
    def get(self, model, id):
        pass
    
    @abstractmethod
    def first(self, model):
        pass
    
    @abstractmethod
    def add(self, instance):
        pass
    
    @abstractmethod
    def commit(self):
        pass
    
    @abstractmethod
    def filter(self, model, condition):
        pass
    
    @abstractmethod
    def all(self, model):
        pass
    
    @abstractmethod
    def ilike(self, column, pattern):
        pass
    
    @abstractmethod
    def create_all(self):
        pass
    
    @abstractmethod
    def bulk_save_objects(self, objects):
        pass
    
    @abstractmethod
    def rollback(self):
        pass
    
    @abstractmethod
    def flush(self):
        pass
    
class SQLAlchemyDatabase(DatabaseInterface):
    def __init__(self):
        self.db = SQLAlchemy()

    def init_db(self, app):
        self.db.init_app(app)

    @property
    def Model(self):
        return self.db.Model

    @property
    def Column(self):
        return self.db.Column

    @property
    def Integer(self):
        return self.db.Integer

    @property
    def String(self):
        return self.db.String

    @property
    def ForeignKey(self):
        return self.db.ForeignKey

    @property
    def relationship(self):
        return self.db.relationship
    
    @property
    def Numeric(self):
        return self.db.Numeric
    
    @property
    def Boolean(self):
        return self.db.Boolean
    
    @property
    def Date(self):
        return self.db.Date
    
    @property
    def Time(self):
        return self.db.Time
    
    @property
    def Enum(self):
        return self.db.Enum
    
    @property
    def Text(self):
        return self.db.Text
    
    @property
    def DateTime(self):
        return self.db.DateTime
    
    @property
    def Float(self):
        return self.db.Float
    
    @property
    def CheckConstraint(self):
        return self.db.CheckConstraint
    
    @property
    def func(self):
        return self.db.func

    def get_session(self):
        return self.db.session
    
    def query(self, model):
        session = self.get_session()
        return session.query(model)
    
    def filter_by(self, query, **conditions):
        return query.filter_by(**conditions)
    
    def joinedload(self, relationship):
        # If it's a simple relationship
        if isinstance(relationship, InstrumentedAttribute):
            return joinedload(relationship)

        # If it's a chain of relationships
        elif isinstance(relationship, tuple):
            if relationship and isinstance(relationship[0], InstrumentedAttribute):
                query = joinedload(relationship[0])
            
            for rel in relationship[1:]:
                if isinstance(rel, InstrumentedAttribute):
                    query = query.joinedload(rel)
            
            return query
    
    def options(self, query, *args):
        for option in args:
            query = query.options(option)
        return query
    
    def order_by(self, query, *args):
        return query.order_by(*args)
    
    def get(self, query, id):
        return query.get(id)
    
    def first(self, query):
        return query.first()
    
    def add(self, instance):
        session = self.get_session()
        session.add(instance)

    def commit(self):
        session = self.get_session()
        session.commit()

    def filter(self, query, condition):
        return query.filter(condition)
    
    def all(self, query):
        return query.all()
    
    def ilike(self, column, pattern):
        return column.ilike(pattern)
    
    def create_all(self):
        self.db.create_all()

    def bulk_save_objects(self, objects):
        session = self.get_session()
        session.bulk_save_objects(objects)
        session.commit()

    def rollback(self):
        session = self.get_session()
        session.rollback()

    def flush(self):
        session = self.get_session()
        session.flush()

class Database:
    def __init__(self, database: DatabaseInterface):
        self._db = database

    def init_db(self, app):
        self._db.init_db(app)

    def set_db(self, database: DatabaseInterface):
        self._db = database

    @property
    def Model(self):
        return self._db.Model

    @property
    def Column(self):
        return self._db.Column

    @property
    def Integer(self):
        return self._db.Integer

    @property
    def String(self):
        return self._db.String

    @property
    def ForeignKey(self):
        return self._db.ForeignKey

    @property
    def relationship(self):
        return self._db.relationship
    
    @property
    def Numeric(self):
        return self._db.Numeric
    
    @property
    def Boolean(self):
        return self._db.Boolean
    
    @property
    def Date(self):
        return self._db.Date
    
    @property
    def Time(self):
        return self._db.Time
    
    @property
    def Enum(self):
        return self._db.Enum
    
    @property
    def Text(self):
        return self._db.Text
    
    @property
    def DateTime(self):
        return self._db.DateTime
    
    @property
    def Float(self):
        return self._db.Float
    
    @property
    def CheckConstraint(self):
        return self._db.CheckConstraint
    
    @property
    def func(self):
        return self._db.func

    def get_session(self):
        return self._db.get_session()
    
    def query(self, model):
        return self._db.query(model)
    
    def filter(self, query, condition):
        return self._db.filter_by(query, condition)
    
    def filter_by(self, query, **conditions):
        return self._db.filter_by(query, **conditions)
    
    def first(self, query):
        return self._db.first(query)
    
    def options(self, query, *args):
        return self._db.options(query, *args)
    
    def all(self, query):
        return self._db.all(query)
    
    def order_by(self, query, *args):
        return self._db.order_by(query, *args)

    def joinedload(self, relationship):
        return self._db.joinedload(relationship)
    
    def ilike(self, column, pattern):
        return self._db.ilike(column, pattern)

    def get(self, query, id):
        return self._db.get(query, id)
    
    def add(self, instance):
        self._db.add(instance)

    def commit(self):
        self._db.commit()

    def flush(self):
        self._db.flush()
    
    def create_all(self):
        self._db.create_all()

    def bulk_save_objects(self, objects):
        self._db.bulk_save_objects(objects)

    def rollback(self):
        self._db.rollback()

# Initalize database
db = Database(SQLAlchemyDatabase())