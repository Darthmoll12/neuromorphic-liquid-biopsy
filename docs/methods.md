# 1. SNN Training

## End-motif SNN Channel Classification Test

Sixteen categories corresponding to sixteen different 5' 4-mer sequences were chosen as follows:

 CCCA, CCAG, CCTG, TAGA, AAAA, CCCC, GGGG, TTTT, ACGT, TGCA, GCAT, ATGC, AATT, TTAA, GGCC, CCGG.

A python script was implemented to generate a FASTA file for each of the above motifs. Each FASTA file contained 1,000 individual sequences, each with a randomized internal sequence, for a total of 16,000 sequences. All sequences were made with a length of 200bp (the smalles length allowed for squigulator simulations). This was done to emulate real cfDNA fragment lengths observed in the bloodstream.

Following this, squiggle data was generated using squigulator (see [environment.md](environment.md)). Each sequence was generated with 1,000 different reads, totalling 16,000 reads for this classification test data set. Therefore, each generated sequence was given 1 read (1,000 reads for 1,000 sequences per motif). This allowed for simple tracking of ground truth for each sequence.