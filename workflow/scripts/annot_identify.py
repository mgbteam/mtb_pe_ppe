#!/usr/bin/env python3

import argparse
import csv
import re

from Bio import SeqIO

parser = argparse.ArgumentParser(
    description="Identify genes with description matching a regex"
)
parser.add_argument(
    "-i", "--input", required=True,
    help="Input GenBank file"
)
parser.add_argument(
    "-r", "--regex", required=True,
    nargs=2, action="append", metavar=("NAME", "REGEX"),
    help="Name and regex to match description, can be specified multiple times"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output TSV file"
)
args = parser.parse_args()

regex_dict = {e[0]: re.compile(e[1]) for e in args.regex}
output = []

for seq_record in SeqIO.parse(args.input, "genbank"):
    for feature in seq_record.features:
        if feature.type == "CDS":
            translation = feature.qualifiers.get("translation", None)

            if translation:
                length = len(translation[0])
            else:
                length = ""

            line = {
                    "Locus Tag": feature.qualifiers.get("locus_tag", [""])[0],
                    "Product": feature.qualifiers.get("product", [""])[0],
                    "Pseudo": "Yes" if "pseudo" in feature.qualifiers else "",
                    "Length": length
            }

            families = []

            for name, regex in regex_dict.items():
                if regex.search(line["Product"]):
                    families.append(name)

            line["Family"] = "; ".join(families)
            output.append(line)

with open(args.output, "w") as f:
    cols = ["Locus Tag", "Family", "Product", "Pseudo", "Length"]
    writer = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
    writer.writeheader()
    writer.writerows(output)
