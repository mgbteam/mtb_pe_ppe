rule phylo_run_paup:
    input:
        paup = "workflow/bin/paup4a168_ubuntu64",
        commands = "results/phylo/add_paup_commands/{domain}/{strain}_{domain}_aligned_paup.nxs"
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
        workflow/bin/paup4a168_ubuntu64 -n '{input.commands}' || true
        [[ -s {output.collapsed_tree} ]]
        """
