# 1. SNN Training

## End-motif SNN Channel Classification Test

Seventeen categories corresponding to seventeen different 5' 4-mer sequences were chosen as follows:

 CCCA, CCAG, CCTG, TAGA, AAAA, CCCC, GGGG, TTTT, ACGT, TGCA, GCAT, ATGC, AATT, TTAA, GGCC, CCGG, and AACG.

Data was generated using squigulator (see [environment.md](environment.md)). All simulated cfDNA fragments were made with a length of 200bp (the minimum value for squigulator simulations). Each sequence was generated with 1,000 different reads, totalling 16,000 reads for this classification test data set.

The internal sequences of each read was randomized, mimicking real nanopore data from cfDNA.