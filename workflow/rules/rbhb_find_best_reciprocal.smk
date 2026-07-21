rule rbhb_find_best_reciprocal:
    input:
        fwd="results/rbhb/best_hits_fwd/{strain}_vs_Orthologs_best_hits.tsv",
        rev="results/rbhb/best_hits_rev/Orthologs_vs_{strain}_best_hits.tsv"
    output:
        "results/rbhb/find_best_reciprocal/{strain}_rbhb.tsv"
    shell:
        """
        echo "Locus Tag\tDB Hit\tUniProtKB\te-value\tbitscore" > '{output}'

        cat '{input.fwd}' | while IFS=$'\t' read -r f1 f2 f3 f4 f5 f6 f7; do
            if grep -q "$f2"$'\t'"$f1"$'\t' '{input.rev}'; then
                name="$(echo "$f2" | cut -d'|' -f2)"
                echo "$f1\t$f2\t$name\t$f6\t$f7"
            fi
        done >> '{output}'
        """
