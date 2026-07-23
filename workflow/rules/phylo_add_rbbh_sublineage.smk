rule phylo_add_rbbh_subf:
    input:
        rbbh = "results/rbbh/add_best_hit_info/{strain}_rbbh.tsv",
        seqs = "results/phylo/extract_domains/{domain}/{strain}_{domain}_domains.faa"
    output:
        "results/phylo/add_rbbh_sublineage/{domain}/{strain}_{domain}_domains.faa"
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/add_rbbh_sublineage.py -f '{input.seqs}' \
                                                -t '{input.rbbh}' \
                                                -c 'Sublineage' \
                                                -o '{output}'
        """
