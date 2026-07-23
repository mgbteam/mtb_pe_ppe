rule predict_family:
    input:
        annot = "results/annot/identify/{strain}_annot.tsv",
        rbbh = "results/rbbh/add_best_hit_info/{strain}_rbbh.tsv",
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
                                                    -i 'RBBH' '{input.rbbh}' \
                                                    -i 'InterPro' '{input.interpro}' \
                                                    -o '{output}'
        """
