rule interpro_run:
    input:
        "results/annot/gbk_to_faa/{strain}.faa"
    output:
        directory("results/interpro/run/{strain}")
    threads:
        config["interpro"]["threads"]
    params:
        folder = config["interpro"]["folder"],
        flags = config["interpro"]["flags"]
    conda:
        "../envs/interproscan.yml"
    shell:
        """
        export LD_LIBRARY_PATH="$CONDA_PREFIX/lib"
        mkdir -p '{output}'
        '{params.folder}/interproscan.sh' -cpu {threads} {params.flags} -i '{input}' -d '{output}'
        """
