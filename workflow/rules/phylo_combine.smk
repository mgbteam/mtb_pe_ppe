rule phylo_combine:
    input:
        expand("results/phylo/draw_tree/{domain}/{{strain}}_{domain}_tree.tsv", domain=config["domains"])
    output:
        "results/phylo/combine/{strain}_phylo.tsv"
    shell:
        """
        head -n1 {input[0]} > {output}
        tail -q -n+2 {input} >> {output}
        """
