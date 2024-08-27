#!/usr/bin/env python3
"""This module defines a function that inserts a new document
into a MongoDB collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection based on kwargs
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id  # Return the _id of the inserted document
