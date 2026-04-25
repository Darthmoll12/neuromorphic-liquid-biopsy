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


def rand_internal_sequence(gen: random.Random, length: int):
    """Generates a random internal sequence. Does not take into account bias observed in cfDNA fragments"""
    return ''.join(gen.choices("ACGT", k=length))


def make_fasta_sequence(motif: str, num_reads: int, output_path: Path, seed: int):
    """Makes num_reads FASTA sequence records for a single motif. Returns number of bytes written"""
    gen = random.Random(seed)
    bytes_written = 0
    with open(output_path, "w") as file:
        for i in range(num_reads):
            internal = rand_internal_sequence(gen, INTERNAL_LENGTH)
            seq = motif + internal
            assert len(seq) == SEQ_LEN, f"Length mismatch: {len(seq)}"
            assert seq[:4] == motif, f"Motif mismatch: {seq[:4]} vs {motif}"
            header = f">{motif}_read{i:05d}"
            record = f"{header}\n{seq}\n"
            file.write(record)
            bytes_written += len(record)
        return bytes_written
    

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out_dir", type=Path, required=True, help="Output directory to store FASTA files.")
    parser.add_argument("--reads_per_motif", type=int, default=1000, help="Number of unique sequences generated per motif")
    parser.add_argument("--master_seed", type=int, default=MASTER_SEED, help=f"seed used to generate random internal sequences. Default: {MASTER_SEED}")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = args.out_dir / "motif_manifest.tsv"
    with open(manifest_path, "w") as mf:
        mf.write("# Stage 1 end-motif reference set\n")
        mf.write(f"# Generated: {datetime.now(timezone.utc).isoformat()}\n")
        mf.write(f"# Master seed: {args.master_seed}\n")
        mf.write(f"# Reads per motif: {args.reads_per_motif}\n")
        mf.write(f"# Reference sequence length: {SEQ_LEN} bp\n")
        mf.write(f"# Internal composition: uniform i.i.d. {{A,C,G,T}}\n")
        mf.write("#\n")
        mf.write("motif\tseed\tfasta_path\tn_sequences\tbytes\n")
 
        for motif in MOTIFS:
            seed = motif_seed(motif, args.master_seed)
            fasta_path = args.out_dir / f"{motif}.fa"
            n_bytes = make_fasta_sequence(motif, args.reads_per_motif, fasta_path, seed)
            mf.write(f"{motif}\t{seed}\t{fasta_path.name}\t"
                     f"{args.reads_per_motif}\t{n_bytes}\n")
            print(f"  [{motif}] seed={seed} -> {fasta_path} "
                  f"({args.reads_per_motif} seqs, {n_bytes:,} bytes)")
 
    print(f"\nManifest: {manifest_path}")
    print(f"Total: {len(MOTIFS)} motifs x {args.reads_per_motif} reads = "
          f"{len(MOTIFS) * args.reads_per_motif:,} reference sequences")


if __name__ == "__main__":
    main()