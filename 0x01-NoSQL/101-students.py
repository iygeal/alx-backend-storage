#!/usr/bin/env python3
"""This script returns all students sorted by average score"""


def top_students(mongo_collection):
    """Returns all students sorted by average score"""

    # Use aggregation pipeline to get average score and sort
    pipeline = [
        {
        "$addFields": {
            "averageScore": {
                "$avg": "$topics.score"
            }
        }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]
    # Run the aggregagtion pipeline
    result = mongo_collection.aggregate(pipeline)

    return list(result)
