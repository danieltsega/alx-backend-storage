#!/usr/bin/env python3
"""
List all documnets
"""


def list_all(mongo_collection):
    """
    List all documents function
    """

    return mongo_collection.find()
