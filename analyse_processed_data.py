"""A script to analyse book data."""

import pandas as pd
import csv
import altair as alt
import vl_convert as vlc
import logging
import json

logging.basicConfig(level=logging.INFO)

def plot_decade_releases(file: str, output_file: str) -> None:
    """A pie chart showing the proportion of books released in each decade."""
    # read csv file
    df = pd.read_csv(file)

    century = df["year"] // 10
    df["decade"] = century * 10

    # counts per decade
    decade_counts = df.groupby("decade").size().reset_index(name="count")

    # chart
    decade_chart = alt.Chart(decade_counts).mark_arc().encode(
        theta="count:Q",
        color="decade:N",
        tooltip=["decade:N", "count:Q"]
    ).properties(title="Number of books released per decade")

    # png
    chart_png = vlc.vegalite_to_png(decade_chart.to_json())
    with open(output_file, "wb") as f:
        f.write(chart_png)

    logging.info(f"Pie chart saved to {output_file}")


def plot_top_authors(file: str, output_file: str) -> None:
    """A sorted bar chart showing the total number of ratings for the ten most-rated authors."""
    # read csv file
    df = pd.read_csv(file)

    # total number of ratings per author
    rating_per_author = df.groupby("author_name")["ratings"].sum().reset_index()
    # top 10
    rating_per_author = rating_per_author.sort_values(by="ratings", ascending=False).head(10)

    # chart
    author_chart = alt.Chart(rating_per_author).mark_bar().encode(
        x="ratings:Q",
        y=alt.Y("author_name:N", sort="-x"),
        color='author_name:N',
        tooltip=["author_name:N", "ratings:Q"]
    ).properties(title="Top 10 most-rated authors")

    # png
    chart_png = vlc.vegalite_to_png(author_chart.to_json())
    with open(output_file, "wb") as f:
        f.write(chart_png)

    logging.info(f"Bar chart saved to {output_file}")


if __name__ == "__main__":
    input_file = "data/PROCESSED_DATA.csv"

    decade_release = "decade_releases.png"
    top_authors = "top_authors.png"

    plot_decade_releases(input_file, decade_release)
    plot_top_authors(input_file, top_authors)
    logging.info("End of script.")
