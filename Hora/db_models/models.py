from datetime import datetime
from mongoengine import connect
from pymongo import MongoClient, ReadPreference
from mongoengine import DynamicDocument, StringField, BooleanField, DateTimeField, \
    DictField, IntField, FloatField, ListField, Document, ReferenceField
from configurations.config import ConfigParser


config_object = ConfigParser()
db_alias_name = config_object.db_alias


def connect_mongo(secondary_preferred=True):
    # if secondary_preferred:
    #     conn_obj = connect(host=connection_uri, alias=db_alias_name, replicaSet=replica_set,
    #                        read_preference=ReadPreference.SECONDARY_PREFERRED)
    # else:
    #     conn_obj = connect(host=connection_uri, alias=db_alias_name, replicaSet=replica_set)
    connection_uri = config_object.get_mongo_db_connection_uri()
    conn_obj = connect(host=connection_uri, alias=db_alias_name)
    return conn_obj


class User(Document):
    """
    Collection Class for storing user documents in mongo
    """
    UserName = StringField(required=True, unique=True)
    Password = StringField()
    FirstName = StringField()
    LastName = StringField()
    Address = StringField()
    IsActive = BooleanField(default=True)
    ModifiedDate = DateTimeField(default=datetime.utcnow)
    meta = {
        'indexes': ['UserName'],
        'index_background': True,
        'collection': 'User',
        'db_alias': db_alias_name
    }


class Category(Document):
    Name = StringField(required=True, unique=True)
    URL = StringField(required=True, unique=True)
    ModifiedDate = DateTimeField(default=datetime.utcnow)
    IsActive = BooleanField(default=True)
    meta = {
        'indexes': ['Name'],
        'index_background': True,
        'collection': 'Category',
        'db_alias': db_alias_name
    }


class Product(Document):
    Category = ReferenceField(Category)
    Name = StringField(required=True)
    URL = StringField(required=True, unique=True)
    OriginalPrice = FloatField(required=True)
    OfferPrice = FloatField(required=True)
    ModifiedDate = DateTimeField(default=datetime.utcnow)
    IsActive = BooleanField(default=True)
    meta = {
        'indexes': [{'fields': ('Name', 'Category'), 'unique': True}],
        'index_background': True,
        'collection': 'Product',
        'db_alias': db_alias_name
    }


class Cart(Document):
    User = ReferenceField(User, required=True)
    Products = ListField(ReferenceField(Product))
    ModifiedDate = DateTimeField(default=datetime.utcnow)
    meta = {
        'indexes': ['User'],
        'index_background': True,
        'collection': 'Cart',
        'db_alias': db_alias_name
    }


class Orders(Document):
    OrderId = StringField(required=True, unique=True)
    User = ReferenceField(User, required=True)
    Products = ListField(ReferenceField(Product))
    ModifiedDate = DateTimeField(default=datetime.utcnow())
    indexes = {
        'indexes': ['User', 'OrderId'],
        'index_background': True,
        'collection': 'Orders',
        'db_alias': db_alias_name
    }

