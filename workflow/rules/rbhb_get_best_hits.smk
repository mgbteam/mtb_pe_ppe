rule rbhb_get_best_hits_fwd:
    input:
        "results/rbhb/blast_fwd/{strain}_vs_Orthologs.tsv"
    output:
        "results/rbhb/best_hits_fwd/{strain}_vs_Orthologs_best_hits.tsv"
    shell:
        """
        sort -k1,1 -k7,7nr '{input}' | sort -u -k1,1 --merge > '{output}'
        """ 


rule rbhb_get_best_hits_rev:
    input:
        "results/rbhb/blast_rev/Orthologs_vs_{strain}.tsv"
    output:
        "results/rbhb/best_hits_rev/Orthologs_vs_{strain}_best_hits.tsv"
    shell:
        """
        sort -k1,1 -k7,7nr '{input}' | sort -u -k1,1 --merge > '{output}'
        """
