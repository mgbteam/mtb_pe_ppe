result_dict_tsv = {
    'Final': 'results/predict/combine/{strain}_predictions.tsv',
    'Annot': 'results/annot/overlap_genes/{strain}_annot.tsv',
    'Overlap': 'results/annot/overlap_regions/{strain}_overlap.tsv',
    'InterPro': 'results/interpro/identify/{strain}_interpro.tsv',
    'Motifs': 'results/motifs/identify/{strain}_motifs.tsv',
    'RBBH': 'results/rbbh/add_best_hit_info/{strain}_rbbh.tsv',
}


def create_input_flags(wildcards):
    for name, file in result_dict_tsv.items():
        yield f"-i '{name}' '{file.format(strain=wildcards.strain)}'"


rule results_to_tsv:
    input:
        [f for f in result_dict_tsv.values()]
    output:
        'results/combined/{strain}_results.tsv'
    params:
        input_flags = create_input_flags
    conda:
        "../envs/python.yml"
    shell:
        """
        workflow/scripts/combine_to_tsv.py -c 'Locus Tag' \
                                           -m 'left' \
                                           {params.input_flags} \
                                           -o '{output}'
        """
