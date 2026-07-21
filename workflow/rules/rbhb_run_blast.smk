rule rbhb_run_blast_fwd:
    input:
        strain_db = "results/rbhb/blast_dbs/{strain}",
        orthologs_db = "results/rbhb/blast_dbs/Orthologs"
    output:
        "results/rbhb/blast_fwd/{strain}_vs_Orthologs.tsv"
    threads:
        config["blastp"]["threads"]
    params:
        flags = config["blastp"]["flags"]
    conda:
        "../envs/blast.yml"
    shell:
        """
        cols='qseqid sseqid pident qlen length evalue bitscore'
        echo "$cols" | sed 's/ /\t/g' > '{output}'
        
        blastp -query '{input.strain_db}/'*.faa \
               -db '{input.orthologs_db}/'*.faa \
               {params.flags} \
               -outfmt '6 qseqid sseqid pident qlen length evalue bitscore' \
               >> {output}
        """


rule rbhb_run_blast_rev:
    input:
        orthologs_db = "results/rbhb/blast_dbs/Orthologs",
        strain_db = "results/rbhb/blast_dbs/{strain}"
    output:
        "results/rbhb/blast_rev/Orthologs_vs_{strain}.tsv"
    threads:
        config["blastp"]["threads"]
    params:
        flags = config["blastp"]["flags"]
    conda:
        "../envs/blast.yml"
    shell:
        """
        cols='qseqid sseqid pident qlen length evalue bitscore'
        echo "$cols" | sed 's/ /\t/g' > '{output}'

        blastp -query '{input.orthologs_db}/'*.faa \
               -db '{input.strain_db}/'*.faa \
               {params.flags} \
               -outfmt "6 $cols" \
               >> {output}
        """
