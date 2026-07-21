#!/usr/bin/env python3

import argparse

import pandas as pd

parser = argparse.ArgumentParser(
    description="Join TSV files by common column"
)
parser.add_argument(
    "-i", "--input", nargs=2, action="append", required=True,
    metavar=("NAME", "FILE"), help="Name and TSV file to combine"
)
parser.add_argument(
    "-c", "--column", required=True,
    help="Column to combine by"
)
parser.add_argument(
    "-s", "--separator", default="\t",
    help="Separator used for input and output (default: \\t)"
)
parser.add_argument(
    "-m", "--method", default="outder",
    help="How to combine: left, right, outer, inner, cross (default: outer)"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output file in TSV format"
)
args = parser.parse_args()

merged = pd.read_csv(args.input[0][1], sep=args.separator)
new_cols = {col: f"{args.input[0][0]} {col}" for col in merged.columns}
new_cols.pop(args.column)
merged = merged.rename(columns=new_cols)

for name, file in args.input[1:]:
    right = pd.read_csv(file, sep=args.separator)
    new_cols = {col: f"{name} {col}" for col in right.columns}
    new_cols.pop(args.column)
    right = right.rename(columns=new_cols)
    merged = pd.merge(merged, right, on=args.column, how=args.method)

merged.to_csv(args.output, sep=args.separator, index=False)
