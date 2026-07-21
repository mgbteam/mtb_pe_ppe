rule predict_combine:
    input:
        family = "results/predict/family/{strain}_family.tsv",
        subfamily = "results/predict/subfamily/{strain}_subfamily.tsv",
        sublineage = "results/phylo/combine/{strain}_phylo.tsv"
    output:
        "results/predict/combine/{strain}_predictions.tsv"
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/combine_to_tsv.py -c 'Locus Tag' \
                                           -m 'left' \
                                           -i Family '{input.family}' \
                                           -i Subfamily '{input.subfamily}' \
                                           -i Sublineage '{input.sublineage}' \
                                           -o '{output}'
        """
