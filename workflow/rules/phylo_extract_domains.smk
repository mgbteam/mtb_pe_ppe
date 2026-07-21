rule phylo_extract_domains:
    input:
        annot = "data/annotation/{strain}.gbff",
        tsv = "results/predict/family/{strain}_family.tsv"
    output:
        "results/phylo/extract_domains/{domain}/{strain}_{domain}_domains.faa"
    params:
        regex = lambda wildcards: config["domains"][wildcards.domain]["regex"],
        nterm_aa = lambda wildcards: config["domains"][wildcards.domain]["nterm_aa"],
        pseudo_flag = "--pseudo" if config["phylogeny"]["pseudo"] else ""
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/extract_domain.py -a '{input.annot}' \
                                           -t '{input.tsv}' \
                                           -n '{wildcards.domain}' \
                                           -l {params.nterm_aa} \
                                           {params.pseudo_flag} \
                                           -o '{output}'
        """
