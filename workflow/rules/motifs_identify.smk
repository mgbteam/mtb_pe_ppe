def create_input_flags(wildcards):
    for motif in config["motifs"]:
        file = f"results/motifs/search/{motif}/{wildcards.strain}_{motif}_motif.tsv"
        min_matches = config["motifs"][motif]["min_matches"]
        yield f"-i '{file}' {min_matches}"


rule motifs_identify:
    input:
        expand("results/motifs/search/{motif}/{{strain}}_{motif}_motif.tsv", motif=config["motifs"])
    output:
        "results/motifs/identify/{strain}_motifs.tsv"
    params:
        input_flags = create_input_flags
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/motifs_identify.py {params.input_flags} -o '{output}'
        """
