#!/usr/bin/env python3

import argparse
import csv

parser = argparse.ArgumentParser(
    description="Check which annotated genes are in a list of provided genes"
)
parser.add_argument(
    "-i", "--input", required=True,
    help="Input TSV file of annotation"
)
parser.add_argument(
    "-g", "--genes", required=True,
    help="Input TSV file of selected genes (must contain Locus Tag column)"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output TSV file"
)
parser.add_argument(
    "-c", "--columns", nargs="+",
    help="list of columns to include (separated by space)"
)
args = parser.parse_args()

genes = {}

with open(args.genes) as f:
    reader = csv.DictReader(f, delimiter="\t")

    for row in reader:
        genes[row["Locus Tag"]] = {}

        for col in args.columns:
            genes[row["Locus Tag"]][col] = row[col]

with open(args.input) as f, open(args.output, "w") as out:
    reader = csv.DictReader(f, delimiter="\t")
    cols = reader.fieldnames + args.columns

    writer = csv.DictWriter(out, fieldnames=cols, delimiter="\t")
    writer.writeheader()

    for row in reader:
        if row["Locus Tag"] in genes:
            for col in args.columns:
                row[col] = genes[row["Locus Tag"]][col]
        else:
            for col in args.columns:
                row[col] = ""

        writer.writerow(row)
