from itertools import product

allowed_chars = "ATCG"


def possible_motif_generator(chars, motif_length):
    "Returns a list of all possible 4-mer end-motifs"
    sequence = ["".join(p) for p in product(chars, repeat=motif_length)]
    return sequence


motifs = possible_motif_generator(allowed_chars, 4)
