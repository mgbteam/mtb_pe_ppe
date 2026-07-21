#!/usr/bin/env python3

import argparse
import csv

from Bio import SeqIO
from Bio.Seq import MutableSeq, Seq
from Bio.SeqRecord import SeqRecord

parser = argparse.ArgumentParser(
    description="Extract N-terminal domains of proteins matching a description"
)
parser.add_argument(
    "-a", "--annot", required=True,
    help="Input GenBank file of annotation"
)
parser.add_argument(
    "-t", "--tsv", required=True,
    help="TSV file containing the predicted gene family"
)
parser.add_argument(
    "-n", "--name", required=True,
    help="Name of the protein domain"
)
parser.add_argument(
    "-l", "--length", type=int, required=True,
    help="Length of N-terminal amino acids to extract"
)
parser.add_argument(
    "-p", "--pseudo", action="store_true",
    help="Also extract N-terminal domains of pseudogenes"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output fasta file of n-terminal domains"
)
args = parser.parse_args()

locus_tags = set()

with open(args.tsv, "r") as f:
    reader = csv.DictReader(f, delimiter="\t")

    for row in reader:
        if row["ID"] == args.name:
            locus_tags.add(row["Locus Tag"])

records = []

for record in SeqIO.parse(args.annot, "genbank"):
    for feature in record.features:
        if feature.type != "CDS":
            continue

        locus_tag = feature.qualifiers.get("locus_tag", [""])[0]
        product = feature.qualifiers.get("product", [""])[0]
        translation = feature.qualifiers.get("translation", [""])[0]

        if not args.pseudo:
            if "pseudo" in feature.qualifiers or not translation:
                continue

        if locus_tag and product and locus_tag in locus_tags:
            if translation:
                seq = Seq(translation[:args.length])
            else:
                nuc = feature.extract(record.seq)
                nuc = nuc[:len(nuc) - (len(nuc) % 3)]
                seq = MutableSeq(nuc.translate(table=11, to_stop=True))
                seq = seq[:args.length]
                seq[0] = "M"

            records.append(SeqRecord(seq, id=locus_tag, description=product))

SeqIO.write(records, args.output, "fasta")
