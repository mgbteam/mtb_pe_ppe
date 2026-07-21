#!/usr/bin/env python3

import argparse
import csv
import re

from Bio import SeqIO

parser = argparse.ArgumentParser(
    description="Find motifs in a set of sequences"
)
parser.add_argument(
    "-i", "--input", required=True,
    help="Input FASTA file"
)
parser.add_argument(
    "-r", "--regex", required=True,
    help="Comma separated list of motif regexes"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output TSV file"
)
parser.add_argument(
    "-n", "--name", default="Hits",
    help="Motif name (default: Hits)"
)
args = parser.parse_args()

regexes = args.regex.split(",")
counts = []

for record in SeqIO.parse(args.input, "fasta"):
    recordseq = str(record.seq)
    count = 0

    for regex in regexes:
        count += len(re.findall(regex, recordseq))

    if count > 0:
        counts.append({"Locus Tag": record.id, args.name: str(count)})
    else:
        counts.append({"Locus Tag": record.id, args.name: ""})

with open(args.output, "w") as outfile:
    fieldnames = ["Locus Tag", args.name]

    writer = csv.DictWriter(outfile, delimiter="\t", fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(counts)
