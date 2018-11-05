from bson.objectid import ObjectId
from pymongo import MongoClient


__mongo = MongoClient('mongodb://localhost:27017/starwars')
__planets_collection = __mongo.db["planets"]


def get_all():
    '''Get all planets.'''
    return __planets_collection.find()

def get_one_by_id(object_id):
    '''Get one planet by its ID.

    Args:
        object_id (bson.objectid.ObjectId): Planet ID.

    Returns:
        dict: Planet data if planet was found, None otherwise.
    '''
    return __planets_collection.find_one({'_id': ObjectId(object_id)})

def get_one_by_name(name):
    '''Get one planet by its name.

    Args:
        name (str): Planet name.

    Returns:
        dict: Planet data if planet was found, None otherwise.
    '''
    return __planets_collection.find_one({'name': name})

def insert_one(data):
    '''Insert one planet in the database.'''
    # TODO check for name duplicates?
    return __planets_collection.insert_one(data).inserted_id

def delete_one(object_id):
    '''Delete one planet by its ID.

    Args:
        object_id (bson.objectid.ObjectId): Planet ID.

    Returns:
        int: Count of deleted objects, or -1 if there was a database problem.
    '''
    result = __planets_collection.delete_one({'_id': ObjectId(object_id)})
    if result.acknowledged is True:
        return result.deleted_count
    else:
        return -1
