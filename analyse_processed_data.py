"""A script to analyse book data."""

import pandas as pd
import csv
import altair as alt
import vl_convert as vlc
import logging
import json

logging.basicConfig(level=logging.INFO)

# def load_data(file: str) -> list[dict]:
#     """Load processed data and returns a list of dicts."""
#     data = []

#     with open(file, "r", encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             # change columns to integers and floats
#             row["year"] = int(row["year"])
#             row["rating"] = float(row["rating"])
#             row["ratings"] = int(row["ratings"])
#             data.append(row)

#     return data


def plot_decade_releases(file: str, output_file: str):
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
    ).properties(title="Proportion of Books Released per Decade")

    # png
    chart_png = vlc.vegalite_to_png(decade_chart.to_json())
    with open(output_file, "wb") as f:
        f.write(chart_png)

    logging.info(f"Pie chart saved to {output_file}")


if __name__ == "__main__":
    input_file = "data/PROCESSED_DATA.csv"
    # book_data = load_data(input_file)

    decade_release = "decade_releases.png"
    top_authors = "top_authors.png"

    plot_decade_releases(input_file, decade_release)
    # plot_decade_releases(book_data)
    # plot_top_authors(book_data)
    # plot_decade_releases(input_file, "decade_releases.png")
    # plot_top_authors(input_file, "top_authors.png")
    logging.info("End of script.")
