rule phylo_run_paup:
    input:
        "results/phylo/add_paup_commands/{domain}/{strain}_{domain}_aligned_paup.nxs"
    output:
        bootstrap_trees = "results/phylo/run_paup/{domain}/{strain}/bootstrap.trees",
        consensus_tree = "results/phylo/run_paup/{domain}/{strain}/consensus.tree",
        collapsed_tree = "results/phylo/run_paup/{domain}/{strain}/consensus_collapsed.tree"
    conda:
        "../envs/paup.yml"
    shell:
        """
		export LD_LIBRARY_PATH="$CONDA_PREFIX/lib"
        mkdir -p "$(dirname '{output.bootstrap_trees}')"
        workflow/bin/paup4a168_ubuntu64 -n '{input}' || true
        [[ -s {output.collapsed_tree} ]]
        """
