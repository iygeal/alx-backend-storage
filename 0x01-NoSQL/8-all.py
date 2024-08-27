#!/usr/bin/env python3
"""This module defines a function that returns list of all
documents in a collection
"""


def list_all(mongo_collection):
    """Lists all documents in a collection or empty list if no documents
    """
    if mongo_collection.count_documents({}) > 0:
        return list(mongo_collection.find())
    else:
        return []
