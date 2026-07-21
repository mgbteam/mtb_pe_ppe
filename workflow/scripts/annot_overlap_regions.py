#!/usr/bin/env python3

import argparse
import csv

from Bio import SeqIO

parser = argparse.ArgumentParser(
    description="Check overlap of RefSeq IDs with BED regions"
)
parser.add_argument(
    "-i", "--input", required=True,
    help="Genome annotation in GenBank format"
)
parser.add_argument(
    "-b", "--bed", required=True,
    help="BED file containing the regions"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output TSV file"
)
args = parser.parse_args()

regions = {}

with open(args.bed, "r") as fi:
    reader = csv.reader(fi, delimiter="\t")

    for row in reader:
        if row[0] not in regions:
            regions[row[0]] = []

        regions[row[0]].append(row)

with open(args.output, "w") as fo:
    writer = csv.writer(fo, delimiter="\t")
    writer.writerow(["Locus Tag", "Regions"])

    for record in SeqIO.parse(args.input, "genbank"):
        for feature in record.features:
            if feature.type != "CDS":
                continue
            if "locus_tag" not in feature.qualifiers:
                continue

            locus_tag = feature.qualifiers["locus_tag"][0]
            start = feature.location.start
            end = feature.location.end
            overlaps = []

            if record.id in regions:
                for region in regions[record.id]:
                    if int(region[1]) <= start <= int(region[2]):
                        overlaps.append(region[3])
                    elif int(region[1]) <= end <= int(region[2]):
                        overlaps.append(region[3])

            writer.writerow([locus_tag, ";".join(overlaps)])
