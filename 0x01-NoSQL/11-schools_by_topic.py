#!/usr/bin/env python3
"""This module defines a function to find schools by topic"""


def schools_by_topic(mongo_collection, topic):
    """Returns the list of school having a specific topic"""
    return mongo_collection.find({"topics": topic})
