#!/usr/bin/env python3

import argparse

from Bio import SeqIO
from Bio.Seq import MutableSeq, Seq
from Bio.SeqRecord import SeqRecord

parser = argparse.ArgumentParser(
    description="Extract protein sequences from GenBank file"
)
parser.add_argument(
    "-i", "--input", required=True,
    help="Input GenBank file"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output FASTA file"
)
args = parser.parse_args()

records = []

for seq_record in SeqIO.parse(args.input, "genbank"):
    for feature in seq_record.features:
        if feature.type == "CDS":
            locus_tag = feature.qualifiers.get("locus_tag", [""])[0]
            product = feature.qualifiers.get("product", [""])[0]
            translation = feature.qualifiers.get("translation", [""])[0]

            if translation:
                pep = Seq(translation)
            else:
                nuc = feature.extract(seq_record.seq)
                nuc = nuc[:len(nuc) - (len(nuc) % 3)]
                pep = MutableSeq(nuc.translate(table=11, to_stop=True))
                pep[0] = "M"

            rec = SeqRecord(id=locus_tag, description=product, seq=pep)
            records.append(rec)

SeqIO.write(records, args.output, "fasta")
