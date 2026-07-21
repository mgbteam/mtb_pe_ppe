#!/usr/bin/env python3

import argparse
import csv
import re

parser = argparse.ArgumentParser(
    description="Parse InterProScan output"
)
parser.add_argument(
    "-i", "--input", required=True,
    help="InterProScan tsv output"
)
parser.add_argument(
    "-r", "--regex", required=True,
    nargs=2, action="append", metavar=("NAME", "REGEX"),
    help="Name and regex to match description, can be specified multiple times"
)
parser.add_argument(
    "-s", "--search", nargs="+", required=True,
    help="Space separated list of analysis to match the regex against"
)
parser.add_argument(
    "-a", "--analysis", nargs="+", required=True,
    help="Space separated list of additional analysis to include in output"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output tsv file"
)
args = parser.parse_args()

cols = [
        "Protein",
        "MD5",
        "Length",
        "Analysis",
        "Signature_accession",
        "Signature_description",
        "Start",
        "End",
        "Score",
        "Status",
        "Date",
        "InterPro_accession",
        "InterPro_description",
]

regex_dict = {e[0]: re.compile(e[1]) for e in args.regex}

output = {}
outcols = ["Locus Tag", "Family"]

for analysis in args.search:
    outcols.extend([f"{analysis} ID", f"{analysis} Description"])

for analysis in args.analysis:
    outcols.append(f"{analysis}")

with open(args.input, "r") as f:
    reader = csv.DictReader(f, delimiter="\t", fieldnames=cols)

    for row in reader:
        protein = row["Protein"]
        analysis = row["Analysis"]

        if protein not in output:
            output[protein] = {"Locus Tag": protein, "Family": []}

        if analysis in args.search:
            id_col = f"{analysis} ID"
            desc_col = f"{analysis} Description"

            if id_col not in output[protein]:
                output[protein][id_col] = set()
                output[protein][desc_col] = set()

            output[protein][id_col].add(row["Signature_accession"])
            output[protein][desc_col].add(row["Signature_description"])
            matching_families = []

            for family, regex in regex_dict.items():
                if regex.search(row["Signature_description"]):
                    matching_families.append(family)

            if matching_families:
                output[protein]["Family"].append(matching_families)

        if analysis in args.analysis:
            output[protein][analysis] = row["Signature_accession"]

for row in output.values():
    if row["Family"]:
        min_matches = min([len(f) for f in row["Family"]])
        families = set()

        for matches in row["Family"]:
            if len(matches) == min_matches:
                for family in matches:
                    families.add(family)

        row["Family"] = "; ".join(families)
    else:
        row["Family"] = ""

    for analysis in args.search:
        if f"{analysis} ID" in row:
            for col in [f"{analysis} ID", f"{analysis} Description"]:
                row[col] = "; ".join(row[col])

with open(args.output, "w") as f:
    writer = csv.DictWriter(f, fieldnames=outcols, delimiter="\t")
    writer.writeheader()
    writer.writerows(output.values())
