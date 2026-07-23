rule rbbh_create_strain_db:
    input:
        "results/annot/gbk_to_faa/{strain}.faa"
    output:
        directory("results/rbbh/blast_dbs/{strain}")
    conda:
        "../envs/blast.yml"
    shell:
        """
        makeblastdb -in '{input}' -dbtype prot -title '{wildcards.strain}'
        mkdir -p '{output}'
        cp '{input}' '{output}'/
        mv '{input}.'* '{output}'/
        """


rule rbbh_create_orthologs_db:
    input:
        "data/orthologs/orthologs.faa"
    output:
        directory("results/rbbh/blast_dbs/Orthologs")
    conda:
        "../envs/blast.yml"
    shell:
        """
        makeblastdb -in '{input}' -dbtype prot -title Orthologs
        mkdir -p '{output}'
        cp '{input}' '{output}'/
        mv '{input}.'* '{output}'/
        """


