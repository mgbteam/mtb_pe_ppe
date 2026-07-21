#!/bin/sh

snakemake --dag | dot -Tpng > dag.png
snakemake --dag | dot -Tsvg > dag.svg
