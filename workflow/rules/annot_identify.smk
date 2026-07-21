rule annot_identify:
    input:
        "data/annotation/{strain}.gbff"
    output:
        "results/annot/identify/{strain}_annot.tsv"
    params:
        regex = " ".join([f"-r '{d}' '{config['domains'][d]['regex']}'" for d in config["domains"]])
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/annot_identify.py -i '{input}' {params.regex} -o '{output}'
        """
