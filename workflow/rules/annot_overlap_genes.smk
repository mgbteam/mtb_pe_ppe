rule annot_overlap_genes:
    input:
        annot = "results/annot/identify/{strain}_annot.tsv",
        genes = "data/genes/{strain}.tsv"
    output:
        "results/annot/overlap_genes/{strain}_annot.tsv"
    params:
        columns = " ".join([f"'{col}'" for col in config['overlap']['gene_columns']])
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/annot_overlap_genes.py -i '{input.annot}' -g '{input.genes}' -o '{output}' -c {params.columns}
        """
