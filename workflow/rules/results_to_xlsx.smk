result_dict_xlsx = {
    'Final Prediction': 'results/predict/combine/{strain}_predictions.tsv',
    'Annotation': 'results/annot/overlap_genes/{strain}_annot.tsv',
    'Overlap': 'results/annot/overlap_regions/{strain}_overlap.tsv',
    'InterProScan': 'results/interpro/identify/{strain}_interpro.tsv',
    'Motif Search': 'results/motifs/identify/{strain}_motifs.tsv',
    'Reciprocal Best BLAST Hit': 'results/rbbh/add_best_hit_info/{strain}_rbbh.tsv',
}


def collect_input(wildcards):
    for file in result_dict_xlsx.values():
        for strain in config["strains"]:
            yield file.format(strain=strain)


def create_input_flags(wildcards):
    for name, file in result_dict_xlsx.items():
        for strain in config["strains"]:
            yield f"-i '{strain}' '{name}' '{file.format(strain=strain)}'"


rule results_to_xlsx:
    input:
        collect_input
    output:
        report("results/results_combined.xlsx", category="Tables")
    params:
        input_flags = create_input_flags
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/combine_to_xlsx.py -c 'Locus Tag' \
                                            -m 'left' \
                                            -s 'Family ID' 'Sublineage ID' 'Subfamily ID' \
                                            {params.input_flags} \
                                            -o '{output}'
        """
