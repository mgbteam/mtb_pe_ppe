rule phylo_add_paup_commands:
    input: 
        fasta = "results/phylo/add_rbbh_sublineage/{domain}/{strain}_{domain}_domains.faa",
        alignment = "results/phylo/align_domains/{domain}/{strain}_{domain}_aligned.nxs"
    output:
        "results/phylo/add_paup_commands/{domain}/{strain}_{domain}_aligned_paup.nxs"
    params:
        outgroup_regex = lambda wildcards: config["domains"][wildcards.domain]["outgroup_regex"],
        seed = config["phylogeny"]["seed"],
        bootstrap = config["phylogeny"]["bootstrap"],
        search = config["phylogeny"]["search"]
    shell:
        """
        cat '{input.alignment}' > '{output}'
        cat config/paup.txt >> '{output}'

        outgroup=$(grep -P '{params.outgroup_regex}' '{input.fasta}' | sed 's/^>//;s/ .*//')
        sed -i "s;{{outgroup}};$outgroup;" '{output}'
        sed -i 's;{{seed}};{params.seed};' '{output}'
        sed -i 's;{{nreps}};{params.bootstrap};' '{output}'
        sed -i 's;{{search}};{params.search};' '{output}'

        outpath="../../../../$(dirname '{output}' | sed 's/add_paup_commands/run_paup/')/{wildcards.strain}"
        echo "$outpath"
        sed -i "s;{{output_trees}};$outpath/bootstrap.trees;" '{output}'
        sed -i "s;{{output_consensus}};$outpath/consensus.tree;" '{output}'
        sed -i "s;{{output_collapsed}};$outpath/consensus_collapsed.tree;" '{output}'
        """
