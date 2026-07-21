#!/usr/bin/env python3

import argparse
import re

import pandas as pd

parser = argparse.ArgumentParser(
    description="Left-join tables by common column"
)
parser.add_argument(
    "-i", "--input", required=True,
    nargs=3, action="append", metavar=("SHEET", "NAME", "FILE"),
    help="Worksheet, name and input tsv file, can be specified multiple times"
)
parser.add_argument(
    "-c", "--column", required=True,
    help="Column to combine by"
)
parser.add_argument(
    "-s", "--sort", nargs="+", default=None, metavar="COLUMN",
    help="Columns in first table to sort by"
)
parser.add_argument(
    "-t", "--separator", default="\t",
    help="Separator used for input and output (default: \\t)"
)
parser.add_argument(
    "-m", "--method", default="outer",
    help="How to combine: left, right, outer, inner, cross (default: outer)"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output file in xlsx format"
)
args = parser.parse_args()

all_tables = {}

# read tables and store them in a dictionary by worksheet
for worksheet, name, file in args.input:
    if worksheet not in all_tables:
        all_tables[worksheet] = {"Names": [], "Tables": []}

    table = pd.read_csv(file, sep=args.separator)
    all_tables[worksheet]["Names"].append(name)
    all_tables[worksheet]["Tables"].append(table)

# define cell formats
writer = pd.ExcelWriter(args.output, engine="xlsxwriter")

odd_top = writer.book.add_format({
    "bg_color": "#bbbbbb",
    "bold": True,
    "align": "center",
})
even_top = writer.book.add_format({
    "bg_color": "#dddddd",
    "bold": True,
    "align": "center"
})
odd_bottom = writer.book.add_format({
    "bg_color": "#bbbbbb",
    "bold": True
})
even_bottom = writer.book.add_format({
    "bg_color": "#dddddd",
    "bold": True
})

on = args.column
how = args.method

# merge the tables per worksheet and convert them to Excel format
for wsname, inputs in all_tables.items():
    merged = inputs["Tables"][0]

    for i in range(1, len(inputs["Tables"])):
        sf = [f"_x{i}", f"_y{i}"]
        merged = merged.merge(inputs["Tables"][i], on=on, how=how, suffixes=sf)
        i += 1

    # sort the merged table by sort_cols if sorting is requested
    if args.sort:
        cols = [inputs["Tables"][0].columns.get_loc(c) for c in args.sort]
        merged.sort_values(by=[merged.columns[i] for i in cols], inplace=True)

    merged.to_excel(writer, sheet_name=wsname, index=False, startrow=1)
    worksheet = writer.sheets[wsname]

    # merge cells in first row based on the width of the tables
    pos = 0
    is_odd = False

    for name, table in zip(inputs["Names"], inputs["Tables"]):
        # remove the merged column if it is not the first table
        if pos > 0:
            table = table.drop(args.column, axis=1)

        ncols = len(table.columns)

        # choose formatting based on whether the merged column is odd or even
        if is_odd:
            top = odd_top
            bottom = odd_bottom
        else:
            top = even_top
            bottom = even_bottom

        # merge cells in the first row if there are more than one column
        if ncols > 1:
            worksheet.merge_range(0, pos, 0, pos + ncols - 1, name, top)
        else:
            worksheet.write(0, pos, name, top)

        # also format the columns in the second row and remove suffixes
        for i in range(ncols):
            col_no_sfx = re.sub(r"_x\d*|_y\d*", "", merged.columns[pos + i])
            worksheet.write(1, pos + i, col_no_sfx, bottom)

        pos += ncols
        is_odd = not is_odd

    # freeze first two rows, autofilter second row and autofit column width
    worksheet.freeze_panes(2, 0)
    worksheet.autofilter(1, 0, 1, pos - 1)
    worksheet.autofit()

writer.close()
