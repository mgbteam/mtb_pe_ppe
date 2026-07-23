#!/usr/bin/env python3

import argparse
import csv

from Bio import SeqIO

parser = argparse.ArgumentParser(
    description="Add RBBH subfamily information to sequence IDs"
)
parser.add_argument(
    "-f", "--fasta", required=True,
    help="Input FASTA file"
)
parser.add_argument(
    "-t", "--table", required=True,
    help="Table containing subfamily information"
)
parser.add_argument(
    "-c", "--column", required=True,
    help="Subfamily column name in table"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output FASTA file"
)
args = parser.parse_args()

with open(args.table, "r") as f:
    reader = csv.DictReader(f, delimiter="\t")
    subfamilies = {r["Locus Tag"]: r[args.column] for r in reader}

records = SeqIO.to_dict(SeqIO.parse(args.fasta, "fasta"))

for record in records.values():
    if record.id in subfamilies:
        record.id += "_" + subfamilies[record.id]

SeqIO.write(records.values(), args.output, "fasta")
