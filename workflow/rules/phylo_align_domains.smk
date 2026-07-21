rule phylo_align_domains:
    input:
        "results/phylo/add_rbhb_sublineage/{domain}/{strain}_{domain}_domains.faa"
    output:
        "results/phylo/align_domains/{domain}/{strain}_{domain}_aligned.nxs"
    conda:
        "../envs/clustalw.yml"
    shell:
        "clustalw -align -type=PROTEIN -output=NEXUS -infile='{input}' -outfile={output}"
