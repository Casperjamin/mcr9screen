SAMPLES =  'samples/samples.yaml'

CASETTE  = 'sequences/references.fasta'
rule build_database:
    input:
        CASETTE
    output:
        comp = "ref/kma_database/reference.comp.b",
        length = "ref/kma_database/reference.length.b",
        name = "ref/kma_database/reference.name",
        seq = "ref/kma_database/reference.seq.b",
    conda:
        "envs/KMA.yaml"
    params:
        name = "ref/kma_database/reference",
    shell:
        "kma index -i {input} -o {params.name}"

rule kma_alignment:
    input:
        forward = lambda wildcards: SAMPLES[wildcards.sample]['forward'],
        reverse = lambda wildcards: SAMPLES[wildcards.sample]['reverse'],
        reference = "ref/kma_database/reference.comp.b"
    params:
        reference = "ref/kma_database/reference",
        output = "output/{sample}/kma_alignment/KMA"
    output:
        aln = "output/{sample}/kma_alignment/KMA.aln",
        frag = "output/{sample}/kma_alignment/KMA.frag.gz",
        fsa = "output/{sample}/kma_alignment/KMA.fsa",
        res ="output/{sample}/kma_alignment/KMA.res",
    conda:
        "envs/KMA.yaml"
    shell:
        "kma -ipe {input.forward} {input.reverse} -o {params.output} -t_db {params.reference}"

