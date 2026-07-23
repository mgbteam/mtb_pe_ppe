rule predict_subfamily:
    input:
        rbbh = "results/rbbh/add_best_hit_info/{strain}_rbbh.tsv",
        motifs = "results/motifs/identify/{strain}_motifs.tsv"
    output:
        "results/predict/subfamily/{strain}_subfamily.tsv"
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/consolidate_predictions.py -m 'Locus Tag' \
                                                    -p 'Subfamily' \
                                                    -i 'RBBH' '{input.rbbh}' \
                                                    -i 'Motifs' '{input.motifs}' \
                                                    -o '{output}'
        """
