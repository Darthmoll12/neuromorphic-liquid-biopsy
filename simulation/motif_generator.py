import argparse
import hashlib
import random
from pathlib import Path
from datetime import datetime, timezone


SEQ_LEN = 200
INTERNAL_LENGTH = SEQ_LEN - 4

MASTER_SEED = 20260424

MOTIFS = ["CCCA", "CCAG", "CCTG", "TAGA", "AAAA", "CCCC", "GGGG", "TTTT", "ACGT", "TGCA", "GCAT", "ATGC", "AATT", "TTAA", "GGCC", "CCGG"]

def motif_seed(motif, master):
    """Derive a reproducible per-motif seed from the master seed + motif"""
    h = hashlib.sha256(f"{master}_{motif}".encode()).digest()
    return int.from_bytes(h[:4], "big")


def rand_internal_sequence(length: int):
    """Generates a random internal sequence. Does not take into account bias observed in cfDNA fragments"""
    return ''.join(random.Random.choices("ACGT", k=length))