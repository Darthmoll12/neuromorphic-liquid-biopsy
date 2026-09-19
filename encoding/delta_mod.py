import time
from pathlib import Path

import h5py
import numpy as np
import torch
from snntorch import spikegen

SCRIPT_DIRECTORY = Path(__file__).parent

hdf5_data_file = SCRIPT_DIRECTORY.parent / "data" / "motif_dataset.h5"
spike_train_hdf5_file = SCRIPT_DIRECTORY.parent / "data" / "encoded_dataset.h5"
vlen_float_type = h5py.vlen_dtype(np.float32)
string_type = h5py.string_dtype(encoding='utf-8')



def create_spike_train(hdf5, delta_threshold: float):
    # Use a starting threshold of 7pA.
    #This was determined by running determine_threshold.py over a series of random nanopore reads.
    with h5py.File(hdf5, "r") as f:
        
        signals = f["signal"]
        motifs = f["motif"]
        raw_signal_lengths = f["raw_signal_length"]

        #iterate through signal data using hdf5py's built-in chunk iterator
        for chunk_slice in signals.iter_chunks():

            #load only current chunk into memory as numpy array
            chunk_data = signals[chunk_slice]
            chunk_motifs = motifs[chunk_slice]
            chunk_signal_lengths = raw_signal_lengths[chunk_slice]
            chunk_data_1D_tensor = [torch.as_tensor(sig) for sig in chunk_data]

            #pad data to a commond length to since torch.tensor() requires common length objects
            max_len = max(len(seq) for seq in chunk_data)
            padded = []
            for seq in chunk_data_1D_tensor:
                pad_len = max_len - len(seq)
                if pad_len > 0:
                    last_val = seq[-1].expand(pad_len)
                    seq = torch.cat([seq, last_val])
                padded.append(seq)

        
            padded_chunk_data = torch.stack(padded)

            # Shape: (max_len, n_reads, 1)
            padded_chunk_tensor = padded_chunk_data.T.unsqueeze(-1)

            #Generate both positive (1.0) and negative (-1.0) spikes
            spike_train = spikegen.delta(padded_chunk_tensor, threshold=delta_threshold, padding=True, off_spike=True)

            #back to (n_reads, max_len)
            spike_train = spike_train.squeeze(-1).T

            #trim to raw_signal_length since tensor still includes the padded region.
            #padding=True makes spikegen.delta preserve input length, so no "-1" here.
            trimmed_spike_train = [spike_train[i, :chunk_signal_lengths[i]] for i in range(len(chunk_signal_lengths))]
            yield trimmed_spike_train, chunk_motifs



with h5py.File(spike_train_hdf5_file, "w") as f:

    dset_spike = f.create_dataset(
        "spike_train",
        shape=(0,),
        maxshape=(None,),
        dtype=vlen_float_type,
        chunks=True
    )
    dset_motif = f.create_dataset(
        "motifs",
        shape=(0,),
        maxshape=(None,),
        dtype=string_type,
        chunks=True
    )

    with h5py.File(hdf5_data_file, "r") as src:
        total_reads = src["signal"].shape[0]

    idx = 0
    start_time = time.perf_counter()

    for spike_train, motifs in create_spike_train(hdf5_data_file, delta_threshold=7.0):
        n = len(spike_train)
        new_size = idx + n
        dset_spike.resize((new_size,))
        dset_motif.resize((new_size,))


        dset_spike[idx:new_size] = [spike.numpy().astype(np.float32) for spike in spike_train]
        dset_motif[idx:new_size] = [motif for motif in motifs]

        idx = new_size
        elapsed = time.perf_counter() - start_time
        pct = 100 * idx / total_reads
        print(f"{idx}/{total_reads} reads ({pct:.1f}%) - {elapsed:.1f}s elapsed", flush=True)


