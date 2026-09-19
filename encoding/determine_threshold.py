from pathlib import Path

import h5py
import numpy as np

SCRIPT_DIRECTORY = Path(__file__).parent
HDF5_PATH = SCRIPT_DIRECTORY.parent / "data" / "motif_dataset.h5"


def sample_delta_x(
    hdf5_path: Path, reads_per_motif: int = 20, seed: int = 0
) -> np.ndarray:
    rng = np.random.default_rng(seed)

    with h5py.File(hdf5_path, "r") as f:
        motifs = f["motif"][:]
        unique_motifs = np.unique(motifs)

        idx = []
        for motif in unique_motifs:
            motif_idx = np.where(motifs == motif)[0]
            idx.append(rng.choice(motif_idx, size=reads_per_motif, replace=False))
        idx = np.sort(np.concatenate(idx))

        signals = [f["signal"][i] for i in idx]

    deltas = np.concatenate([np.diff(sig) for sig in signals])
    return deltas, len(unique_motifs), len(idx)


if __name__ == "__main__":
    deltas, n_motifs, n_reads = sample_delta_x(HDF5_PATH)
    abs_deltas = np.abs(deltas)

    print(f"motifs sampled: {n_motifs}, reads sampled: {n_reads}")
    print(f"n samples: {abs_deltas.size}")
    print(f"mean |dx|: {abs_deltas.mean():.4f}")
    print(f"std  |dx|: {abs_deltas.std():.4f}")
    for p in (50, 75, 85, 90, 95, 99):
        print(f"p{p}: {np.percentile(abs_deltas, p):.4f}")
