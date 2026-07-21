rule predict_subfamily:
    input:
        rbhb = "results/rbhb/add_best_hit_info/{strain}_rbhb.tsv",
        motifs = "results/motifs/identify/{strain}_motifs.tsv"
    output:
        "results/predict/subfamily/{strain}_subfamily.tsv"
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/consolidate_predictions.py -m 'Locus Tag' \
                                                    -p 'Subfamily' \
                                                    -i 'RBHB' '{input.rbhb}' \
                                                    -i 'Motifs' '{input.motifs}' \
                                                    -o '{output}'
        """
