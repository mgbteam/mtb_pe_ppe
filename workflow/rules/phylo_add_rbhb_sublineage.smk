rule phylo_add_rbhb_subf:
    input:
        rbhb = "results/rbhb/add_best_hit_info/{strain}_rbhb.tsv",
        seqs = "results/phylo/extract_domains/{domain}/{strain}_{domain}_domains.faa"
    output:
        "results/phylo/add_rbhb_sublineage/{domain}/{strain}_{domain}_domains.faa"
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/add_rbhb_sublineage.py -f '{input.seqs}' \
                                                -t '{input.rbhb}' \
                                                -c 'Sublineage' \
                                                -o '{output}'
        """
