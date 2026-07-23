rule rbbh_add_best_hit_info:
    input:
        rbbh="results/rbbh/find_best_reciprocal/{strain}_rbbh.tsv",
        info="data/orthologs/orthologs.tsv"
    output:
        "results/rbbh/add_best_hit_info/{strain}_rbbh.tsv"
    shell:
        """
        join -t $'\t' \
             -1 3 \
             -2 4 --header \
             <(head -n1 '{input.rbbh}'; tail -n+2 '{input.rbbh}' | sort -t $'\t' -k3,3) \
             <(head -n1 '{input.info}'; tail -n+2 '{input.info}' | sort -t $'\t' -k4,4) \
             | sort -t $'\t' -k13,13n -k6,6 -k11,11 \
             > '{output}'
        """
