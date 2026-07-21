#!/usr/bin/env python3

import argparse
import csv

parser = argparse.ArgumentParser(
    description="Final prediction based on provided files (by order of input)"
)
parser.add_argument(
    "-i", "--input", nargs=2, required=True, action="append",
    metavar=("NAME", "FILE"), help="Name and input TSV file of analysis"
)
parser.add_argument(
    "-m", "--mergecol", required=True,
    help="Name of column to merge on"
)
parser.add_argument(
    "-p", "--predcol", required=True,
    help="Name of column to use for prediction"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output TSV file"
)
args = parser.parse_args()

files = {e[0]: e[1] for e in args.input}
output = {}

for name, file in files.items():
    with open(file, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for row in reader:
            locus_tag = row[args.mergecol]

            if locus_tag not in output:
                if row[args.predcol]:
                    output[locus_tag] = {
                            args.mergecol: locus_tag,
                            "ID": row[args.predcol],
                            "Src": name
                    }
            else:
                output_pred_count = len(output[locus_tag]["ID"].split("; "))
                row_pred_count = len(row[args.predcol].split("; "))

                # if the prediction is more specific (fewer entries), overwrite
                if row_pred_count < output_pred_count:
                    output[locus_tag]["ID"] = row[args.predcol]
                    output[locus_tag]["Src"] = name

with open(args.output, "w") as f:
    cols = [args.mergecol, "ID", "Src"]
    writer = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
    writer.writeheader()
    writer.writerows(output.values())
