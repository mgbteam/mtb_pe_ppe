rule annot_gbk_to_faa:
    input:
        "data/annotation/{strain}.gbff"
    output:
        "results/annot/gbk_to_faa/{strain}.faa"
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/gbk_to_faa.py -i '{input}' -o '{output}'
        """
