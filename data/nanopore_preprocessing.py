import platform
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
import pyslow5 as ps5


def resolve_windows_path(windows_path: str) -> Path:
    """Translate a C:/... path to /mnt/c/... when running under WSL."""
    if "microsoft" in platform.uname().release.lower():
        drive, rest = windows_path.split(":", 1)
        return Path(f"/mnt/{drive.lower()}{rest}")
    return Path(windows_path)


DATA_DIRECTORY = resolve_windows_path(
    "C:/Projects/neuromorphic_liquid_biopsy_data/squiggle"
)
SCRIPT_DIRECTORY = Path(__file__).parent
manifest = pd.read_csv(SCRIPT_DIRECTORY / "motif_manifest.tsv", sep="\t", comment="#")

# initialize hdf5 file parameters
hdf5_file_output = SCRIPT_DIRECTORY / "motif_dataset.h5"
vlen_float_type = h5py.vlen_dtype(np.float32)
string_type = h5py.string_dtype(encoding="utf-8")


def iter_squiggle_reads(manifest_df, data_directory: Path, pA=True):
    for _, row in manifest_df.iterrows():
        blow5path = data_directory / f"{row['motif']}.blow5"
        s5 = ps5.Open(str(blow5path), "r")
        reads = list(s5.seq_reads_multi(threads=4, batchsize=500, pA=True))
        yield reads, row["motif"], blow5path.name


with h5py.File(hdf5_file_output, "w") as f:
    dset_read_id = f.create_dataset(
        "read_id", shape=(0,), maxshape=(None,), dtype=string_type, chunks=True
    )
    dset_sampling_rate = f.create_dataset(
        "sampling_rate", shape=(0,), maxshape=(None,), dtype=np.float64, chunks=True
    )
    dset_raw_signal_length = f.create_dataset(
        "raw_signal_length", shape=(0,), maxshape=(None,), dtype=np.int64, chunks=True
    )
    dset_signal = f.create_dataset(
        "signal", shape=(0,), maxshape=(None,), dtype=vlen_float_type, chunks=True
    )
    dset_motif = f.create_dataset(
        "motif", shape=(0,), maxshape=(None,), dtype=string_type, chunks=True
    )
    dset_filename = f.create_dataset(
        "filename", shape=(0,), maxshape=(None,), dtype=string_type, chunks=True
    )

    idx = 0

    for reads, motif, filename in iter_squiggle_reads(manifest, DATA_DIRECTORY):
        # 1. Expand each dataset by 1,000 (each motif contains 1,000 reads)
        n = len(reads)
        new_size = idx + n

        for dset in (
            dset_read_id,
            dset_sampling_rate,
            dset_raw_signal_length,
            dset_signal,
            dset_motif,
            dset_filename,
        ):
            dset.resize((new_size,))

        # 2. Then write the values
        dset_read_id[idx:new_size] = [r["read_id"] for r in reads]
        dset_sampling_rate[idx:new_size] = [r["sampling_rate"] for r in reads]
        dset_raw_signal_length[idx:new_size] = [r["len_raw_signal"] for r in reads]
        dset_signal[idx:new_size] = [
            np.asarray(r["signal"], dtype=np.float32) for r in reads
        ]
        dset_motif[idx:new_size] = [motif] * n
        dset_filename[idx:new_size] = [filename] * n

        idx += n
