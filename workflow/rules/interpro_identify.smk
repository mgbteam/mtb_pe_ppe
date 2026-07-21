rule interpro_identify:
    input:
        "results/interpro/run/{strain}"
    output:
        "results/interpro/identify/{strain}_interpro.tsv"
    params:
        regex = " ".join([f"-r '{d}' '{config['domains'][d]['regex']}'" for d in config["domains"]]),
        search = config["interpro"]["search"],
        analyses = config["interpro"]["analyses"]
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/interpro_identify.py -i '{input}'/*.tsv \
                                              {params.regex} \
                                              -s {params.search} \
                                              -a {params.analyses} \
                                              -o '{output}'
        """
