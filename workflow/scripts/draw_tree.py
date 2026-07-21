#!/usr/bin/env python3

import argparse
import csv
import os

import ete3

os.environ["QT_QPA_PLATFORM"] = "offscreen"

parser = argparse.ArgumentParser(
    description="Draw tree colored by sublineage"
)
parser.add_argument(
    "-i", "--input", required=True,
    help="Input Newick tree file"
)
parser.add_argument(
    "-c", "--color", nargs=2, action="append", metavar=("NAME", "COLOR"),
    help="Name and color of sublineage, can be specified multiple times"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output image file"
)
parser.add_argument(
    "-t", "--tsv",
    help="Output tsv file of inferred subfamilies"
)
args = parser.parse_args()

t = ete3.Tree(args.input)
t.ladderize()

ts = ete3.TreeStyle()
ts.show_leaf_name = True
ts.show_branch_length = False
ts.show_branch_support = True
ts.show_scale = False
ts.scale = 32

colors = {name: color for name, color in args.color}
mapping = {}

for n in t.traverse():
    if n.is_leaf():
        continue

    subfamilies = set()

    for leaf in n.get_leaves():
        sublineage = leaf.name.split("_")[-1]

        if sublineage in colors:
            subfamilies.add(sublineage)
            locus_tag = leaf.name.removesuffix("_" + sublineage)
            mapping[leaf.name] = {"Locus Tag": locus_tag, "ID": sublineage}
        else:
            mapping[leaf.name] = {"Locus Tag": leaf.name, "ID": ""}

    if len(subfamilies) == 1:
        sublineage = subfamilies.pop()

        for leaf in n.get_leaves():
            locus_tag = leaf.name.removesuffix("_" + sublineage)
            mapping[leaf.name] = {"Locus Tag": locus_tag, "ID": sublineage}

        if sublineage in colors:
            for node in n.traverse():
                node.img_style["hz_line_color"] = colors[sublineage]
                node.img_style["vt_line_color"] = colors[sublineage]
                node.img_style["fgcolor"] = colors[sublineage]

t.render(args.output, h=960, tree_style=ts)

if args.tsv is not None:
    with open(args.tsv, "w") as f:
        outcols = ["Locus Tag", "ID"]
        writer = csv.DictWriter(f, fieldnames=outcols, delimiter="\t")
        writer.writeheader()
        writer.writerows(mapping.values())
