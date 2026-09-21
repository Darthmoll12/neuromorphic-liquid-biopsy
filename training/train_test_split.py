import numpy as np
import h5py
from pathlib import Path
from sklearn.model_selection import train_test_split

SCRIPT_DIRECTORY = Path(__file__).parent

encoded_hdf5_file = SCRIPT_DIRECTORY.parent / "data" / "encoded_dataset.h5"
np_array_path = SCRIPT_DIRECTORY.parent / "data" / "train_test_split_idx.npz"


def get_train_test_split_indices(hdf5):
    """
    Creates an evenly-spaced array with the same length as the number of reads in the dataset.
    Returns arrays containing indices of reads belonging to train, test, and validation datasets.
    Train/Test/Val split is 80/10/10.
    """
    print(f"Loading motif labels from {hdf5}...")
    with h5py.File(hdf5, "r") as f:
        Y = f["motifs"][:]
        num_reads = len(Y)
        index_array = np.arange(num_reads)
        print(f"Loaded {num_reads} reads.")

        print("Splitting off test set (10%)...")
        idx_train_val, idx_test, Y_train_val, Y_test = train_test_split(
            index_array, Y, test_size=0.10, random_state=42, stratify=Y
        )

        print("Splitting remainder into train/val (90/10 of remainder)...")
        idx_train, idx_val, Y_train, Y_val = train_test_split(
            idx_train_val, Y_train_val, test_size=0.111,
            random_state=42, stratify=Y_train_val
        )

        print(f"train: {len(idx_train)}, val: {len(idx_val)}, test: {len(idx_test)}")

        return idx_train, idx_val, idx_test, Y_train, Y_val, Y_test
    


idx_train, idx_val, idx_test, Y_train, Y_val, Y_test = get_train_test_split_indices(encoded_hdf5_file)

print(f"Saving split indices to {np_array_path}...")
np.savez(np_array_path, idx_train=idx_train, idx_val=idx_val, idx_test=idx_test,
         Y_train=Y_train, Y_val=Y_val, Y_test=Y_test)
print("Done.")





