rule annot_overlap_regions:
    input:
        annot = "data/annotation/{strain}.gbff",
        regions = "data/regions/{strain}.bed"
    output:
        "results/annot/overlap_regions/{strain}_overlap.tsv"
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/annot_overlap_regions.py -i '{input.annot}' -b '{input.regions}' -o '{output}'
        """
