#!/usr/bin/env python3
"""
List documents by topic
"""

def schools_by_topic(mongo_collection, topic):
    """
    List documents by topic
    """

    return mongo_collection.find({"topics": topic})
