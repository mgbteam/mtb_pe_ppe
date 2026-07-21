#!/usr/bin/env python3

import argparse
import csv

parser = argparse.ArgumentParser(
    description="This script identifies gene subfamilies by motif"
)
parser.add_argument(
    "-i", "--input", required=True,
    nargs=2, action="append", metavar=("FILE", "MIN_COUNT"),
    help="Input TSV and minimum motif count, can be specified multiple times"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output TSV file"
)
args = parser.parse_args()

output = {}
outcols = ["Locus Tag", "Subfamily"]

for file, min_count in args.input:
    with open(file, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        motif = reader.fieldnames[1]
        outcols.append(motif)

        for row in reader:
            if row["Locus Tag"] not in output:
                new_row = {"Locus Tag": row["Locus Tag"], "Subfamily": []}
                output[row["Locus Tag"]] = new_row

            count = int(row[motif]) if row[motif] else 0
            output[row["Locus Tag"]][motif] = count

            if count >= int(min_count):
                output[row["Locus Tag"]]["Subfamily"].append(motif)

with open(args.output, "w") as f:
    writer = csv.DictWriter(f, fieldnames=outcols, delimiter="\t")
    writer.writeheader()

    for row in output.values():
        if row["Subfamily"]:
            row["Subfamily"] = "; ".join(row["Subfamily"])
        else:
            row["Subfamily"] = ""

        writer.writerow(row)
