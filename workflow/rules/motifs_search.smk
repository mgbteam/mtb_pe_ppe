rule motifs_search:
    input:
        "results/annot/gbk_to_faa/{strain}.faa"
    output:
        "results/motifs/search/{motif}/{strain}_{motif}_motif.tsv"
    params:
        regex = lambda wildcards: ",".join(config["motifs"][wildcards.motif]["regex"])
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/motifs_search.py -i '{input}' \
                                          -n '{wildcards.motif}' \
                                          -r '{params.regex}' \
                                          -o '{output}'
        """
