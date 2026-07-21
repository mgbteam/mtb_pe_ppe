rule predict_family:
    input:
        annot = "results/annot/identify/{strain}_annot.tsv",
        rbhb = "results/rbhb/add_best_hit_info/{strain}_rbhb.tsv",
        interpro = "results/interpro/identify/{strain}_interpro.tsv"
    output:
        "results/predict/family/{strain}_family.tsv"
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/consolidate_predictions.py -m 'Locus Tag' \
                                                    -p 'Family' \
                                                    -i 'Annotation' '{input.annot}' \
                                                    -i 'RBHB' '{input.rbhb}' \
                                                    -i 'InterPro' '{input.interpro}' \
                                                    -o '{output}'
        """
