rule rbhb_add_best_hit_info:
    input:
        rbhb="results/rbhb/find_best_reciprocal/{strain}_rbhb.tsv",
        info="data/orthologs/orthologs.tsv"
    output:
        "results/rbhb/add_best_hit_info/{strain}_rbhb.tsv"
    shell:
        """
        join -t $'\t' \
             -1 3 \
             -2 4 --header \
             <(head -n1 '{input.rbhb}'; tail -n+2 '{input.rbhb}' | sort -t $'\t' -k3,3) \
             <(head -n1 '{input.info}'; tail -n+2 '{input.info}' | sort -t $'\t' -k4,4) \
             | sort -t $'\t' -k13,13n -k6,6 -k11,11 \
             > '{output}'
        """
