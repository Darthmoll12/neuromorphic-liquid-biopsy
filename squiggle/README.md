# squiggle/

Squigulator-generated synthetic nanopore squiggle output (`.blow5` + `.paf` per 4-mer end-motif),
one pair per motif in `simulation/sequence_generator.py`'s `MOTIFS` list.

These files are large (~1.1GB total) and fully reproducible from the seeded FASTA references in
`refs/`, so the generated data itself lives outside the repo at:

    ../neuromorphic_liquid_biopsy_data/squiggle/

Not tracked in git (see `.gitignore`: `*.blow5`, `*.paf`).
