#!/usr/bin/env python3
"""
Insert a document
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a document
    """

    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id
