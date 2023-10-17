#!/usr/bin/env python3
"""
Return average
"""


def top_students(mongo_collection):
    """
    Return average
    """
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])
