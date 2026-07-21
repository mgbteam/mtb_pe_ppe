def create_color_flags(wildcards):
    flags = []

    for n, c in config["domains"][wildcards.domain]["sublineage_colors"].items():
        flags.append(f"-c '{n}' '{c}'")

    return " ".join(flags)


rule phylo_draw_tree:
    input:
        "results/phylo/run_paup/{domain}/{strain}/consensus_collapsed.tree",
    output:
        figure = report("results/phylo/draw_tree/{domain}/{strain}_{domain}_tree.png", category="Phylogeny", subcategory="{domain}"),
        table = "results/phylo/draw_tree/{domain}/{strain}_{domain}_tree.tsv"
    params:
        colors = create_color_flags
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/draw_tree.py -i '{input}' {params.colors} -o '{output.figure}' -t '{output.table}'
        """
