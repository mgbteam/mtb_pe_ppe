#!/usr/bin/env python3

import argparse

import pandas as pd

parser = argparse.ArgumentParser(
    description="Summarize table by columns"
)
parser.add_argument(
    "-i", "--input", required=True,
    nargs=2, action="append", metavar=("NAME", "FILE"),
    help="Name and input TSV file, can be specified multiple times"
)
parser.add_argument(
    "-o", "--output", required=True,
    help="Output file in TSV format"
)
parser.add_argument(
    "-p", "--pseudo", action="store_true",
    help="Include pseudogenes"
)
args = parser.parse_args()

analyses = {
    "Family": ["Final Family ID"],
    "Subfamily": ["Final Family ID", "Final Subfamily ID"],
    "Sublineage": ["Final Family ID", "Final Sublineage ID"],
    "Illumina": ["Annot Illumina", "Final Family ID"],
    "Overlap": ["Overlap Regions", "Final Family ID"],
    "Pseudo": ["Annot Pseudo", "Final Family ID"],
}

cols = ["Analysis", "Category", "Subcategory"]
result = pd.DataFrame(columns=cols)

for name, file in args.input:
    df = pd.read_csv(file, sep="\t")
    df_nopseudo = df[df["Annot Pseudo"] != "Yes"]
    strain_result = pd.DataFrame()

    for analysis, columns in analyses.items():
        if not args.pseudo and analysis != "Pseudo":
            group = df_nopseudo.groupby(columns).size().reset_index()
        else:
            group = df.groupby(columns).size().reset_index()

        group = group.rename(columns={0: name})
        group["Analysis"] = analysis
        group["Category"] = group[columns[0]]

        if len(columns) == 2:
            group["Subcategory"] = group[columns[1]]
        else:
            group["Subcategory"] = ""

        group = group.drop(columns=columns)
        strain_result = pd.concat([strain_result, group])

    result = pd.merge(result, strain_result, on=cols, how="outer")

result.fillna(0, inplace=True)
result = result.replace(to_replace=".*; .*", value="Unclear", regex=True)

# order by analyses dictionary
result["Analysis"] = result["Analysis"].astype("category")
result["Analysis"] = result["Analysis"].cat.set_categories(analyses.keys())
result = result.sort_values(cols).reset_index(drop=True)

# convert to excel and auto-adjust column width
writer = pd.ExcelWriter(args.output, engine="xlsxwriter")
result.to_excel(writer, sheet_name="Summary", index=False)
ws = writer.sheets["Summary"]

# merge cells the two first columns if they have the same value
style = writer.book.add_format({"bold": True, "valign": "vcenter"})

for i in range(2):
    prev = 1

    for j in range(1, len(result)):
        if result.iloc[j, i] != result.iloc[j - 1, i]:
            if j != prev:
                ws.merge_range(prev, i, j, i, result.iloc[j-1, i], style)
            else:
                ws.write(prev, i, result.iloc[j-1, i], style)

            prev = j + 1

    if prev != j + 1:
        ws.merge_range(prev, i, j+1, i, result.iloc[j, i], style)
    else:
        ws.write(j+1, i, result.iloc[j, i], style)

ws.autofit()
writer.close()
