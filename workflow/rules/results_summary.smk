rule results_summary:
    input:
        expand("results/combined/{strain}_results.tsv", strain=config["strains"])
    output:
        report("results/results_summary.xlsx", category="Tables")
    params:
        input_flags = lambda wildcards: [f"-i {strain} results/combined/{strain}_results.tsv" for strain in config["strains"]],
        pseudo_flag = lambda wildcards: "--pseudo" if config["summary"]["pseudo"] else ""
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/results_summary.py {params.input_flags} \
                                            {params.pseudo_flag} \
                                            -o '{output}'
        """
