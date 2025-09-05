"""A script to process book data."""

import pandas as pd
import csv
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

def clean_title(title: str) -> str:
    """Clean the book title returning the main title."""
    if not title:
        return None
    
    main_title = title.split("(")[0]
    clean_title = main_title.strip()
    return clean_title

def clean_rating(rating: str) -> float:
    """Clean rating column, returning a float."""
    if rating:
        return float(rating.replace(",", "."))
    else:
        return None

def clean_ratings(ratings: str) -> int:
    """Clean ratings column, returning an integer."""
    if ratings:
        return int(ratings.replace("`", ""))
    else:
        return None
    
def clean_full_data(file: str, database):
    """Clean all of the data."""

    rows = []

    with open(file, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            author_id = row["author_id"]

            author_map = get_author_mapping(database)
            author_name = author_map.get(author_id)


if __name__ == "__main__":
    logging.info("Processing started")
    print(get_author_mapping("data/authors.db"))



