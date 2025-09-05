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

def clean_author_id(author_id: str) -> int:
    """Clean author_id returning an integer."""
    clean_author_id = author_id.replace(".", "")
    if author_id and clean_author_id.isdigit():
        return int(float(author_id))
    else:
        return None

def clean_title(title: str) -> str:
    """Clean the book title returning the main title."""
    if not title:
        return None
    
    main_title = title.split("(")[0]
    clean_title = main_title.strip()
    return clean_title


def clean_year(year: str) -> int:
    """Clean year column, returning an int."""
    if year and year.isdigit():
        return int(year)
    else:
        return None

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
    
def get_rating_value(row: dict) -> float:
    """Extract rating value for sorting."""
    if row["rating"] is not None:
        return row["rating"]
    else:
        return 0.0


def clean_full_data(file: str, database, output_file: str):
    """Clean all of the data and output into a csv file."""

    output_rows = []
    author_map = get_author_mapping(database)

    with open(file, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:

            title = clean_title(row["book_title"])
            author_id = clean_author_id((row["author_id"]))
            year = clean_year(row["Year released"])
            rating = clean_rating(row["Rating"])
            ratings = clean_ratings(row["ratings"])

            author_name = author_map.get(author_id)

            if title and author_name and year and rating and ratings:
                output_rows.append({
                    "title" : title,
                    "author_name": author_name,
                    "year": year,
                    "rating": rating,
                    "ratings": ratings
                })
    
    # order rows
    ordered_rows = sorted(output_rows, key=get_rating_value, reverse=True)

    # remove exisiting file
    if path.exists(output_file):
        remove(output_file)
    
    # write to csv
    with open(output_file, "w") as f:
        columns = ["title", "author_name", "year", "rating", "ratings"]
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(ordered_rows)

    logging.info("CSV file successfully written.")

    return ordered_rows


def get_command_line_arguments():
    """Extract command line arguments."""
    # read the argument variable
    parser = ArgumentParser(
        description="Command lines for raw csv files into an output file.")

    parser.add_argument("file", help="The CSV file inputted",type=str)

    # read the argument variable
    args = parser.parse_args()
    return args.file


if __name__ == "__main__":
    logging.info("Processing started")
    file = get_command_line_arguments()

    database = "data/authors.db"
    output_file = "PROCESSED_DATA_4.csv"

    print(clean_full_data(file, database, output_file))



