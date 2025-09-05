"""A script to process book data."""

import pandas as pd
import sqlite3
from os import makedirs, path, remove
from argparse import ArgumentParser
import logging

# right now, there's ,index,Unnamed: 0,book_title,author_id,Year released,Rating,ratings
# we want book title, author_name, year, rating, ratings

def get_author_mapping(database) -> dict:
    """Return a dict mapping with author_id and author_name."""
    conn = sqlite3.connect(database)

    cursor = conn.cursor() 
    cursor.execute("SELECT id, name FROM author;")
    author_data = cursor.fetchall()
    author_mapping_conversion = {row[0]: row[1] for row in author_data}
    conn.close()
    return author_mapping_conversion



if __name__ == "__main__":
    logging.info("Processing started")
    print(get_author_mapping("data/authors.db"))

