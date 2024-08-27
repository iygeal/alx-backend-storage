#!/usr/bin/env python3
"""This module defines a function to update the topics of a 'school'
document based on its name attribute
"""


def update_topics(mongo_collection, name, topics):
    """Updates the topics of a 'school' document based on its name attribute
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
