rule install_paup:
    input:
    output:
        "workflow/bin/paup4a168_ubuntu64"
    shell:
        """
        wget -O '{output}.gz' https://phylosolutions.com/paup-test/paup4a169_ubuntu64.gz
        gzip -d '{output}.gz'
        chmod +x '{output}'
        """
