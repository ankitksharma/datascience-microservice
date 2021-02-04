import numpy as np
from scipy.signal import find_peaks
import scipy.fftpack as fftpack
import math
import matplotlib.pyplot as plt


def calc_bpm(a, fps):
    bucket_size_secs = 10
    max_bpm_diff_for_mean = 20
    freq_limits = (50.0 / 60, 180.0 / 60)

    y2 = np.array(a)  # np.array(rolling_average(a, rolling_average_n)).flatten()

    sum_max_freq = 0
    sum_avg_bps = 0
    max_bps = -1
    min_bps = 10
    bucket_i = 0
    plt.figure(figsize=(40, 32))
    while True:
        bucket = y2[int(bucket_i * bucket_size_secs * fps): int(
            (bucket_i + 1) * bucket_size_secs * fps)]  # use decay weights
        if bucket.shape[0] <= 0: break
        sig_fft, power, sample_freq = get_fft_sig(bucket, 1 / fps)
        max_fq_arr = find_max_within_range(power, sample_freq, freq_limits, 2)
        max_fq, min_fq = max(max_fq_arr), min(max_fq_arr)
        max_fq_mean = np.mean(max_fq_arr) if abs(max_fq - min_fq) * 60 <= max_bpm_diff_for_mean else max_fq
        if not math.isnan(max_fq_mean):
            sum_max_freq += max_fq_mean
        bucket_i += 1
        plt.subplot(3, 3, bucket_i)
        plt.plot(
            sample_freq[np.logical_and(sample_freq > freq_limits[0], sample_freq < freq_limits[1])] * 60,
            (power[np.logical_and(sample_freq > freq_limits[0], sample_freq < freq_limits[1])]))
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('plower')
        peaks2, _ = find_peaks(bucket, distance=7.5, prominence=2)  # BEST!
        max_bps = max(max_bps, peaks2.shape[0] * fps / bucket.shape[0])
        min_bps = min(min_bps, peaks2.shape[0] * fps / bucket.shape[0])
        bucket_bps = peaks2.shape[0] * fps / (bucket.shape[0])
        print(f'{bucket_i} {bucket_bps * 60} {max_fq_arr * 60} {sum_max_freq * 60}')
        sum_avg_bps += bucket_bps
    avg_bps = sum_avg_bps / bucket_i
    avg_max_freq = sum_max_freq / bucket_i
    plt.show()
    return avg_max_freq * 60


def get_max_power_frequencies(bucket, fps, freq_limits):
    sig_fft, power, sample_freq = get_fft_sig(bucket, 1 / fps)
    return find_max_within_range(power, sample_freq, freq_limits, 2)


def find_max_within_range(sig_val, sig, req_range, n_max):
    plt.figure(figsize=(40, 32))
    filtered_sig_indices = np.logical_and(sig >= req_range[0], sig <= req_range[
        1])  # np.logical_and(sample_freq > freq_limits[0], sample_freq < freq_limits[1])
    filtered_sig = sig[filtered_sig_indices]
    filtered_sig_val = sig_val[filtered_sig_indices]
    n_max_arg_partitioned = np.argpartition(filtered_sig_val, -n_max)
    n_max_sig_vals = n_max_arg_partitioned[-n_max:]
    n_max_sig_vals_sorted_index = np.argsort(filtered_sig_val[n_max_sig_vals])
    a3 = filtered_sig[n_max_sig_vals]
    plt.subplot(1, 3, 1)
    for i_x, i_y in zip(np.arange(filtered_sig_val.shape[0]), filtered_sig_val):
        plt.text(i_x, i_y, '({})'.format(round(i_x, 2)))
    plt.plot(filtered_sig_val)
    plt.subplot(1, 3, 2)
    plt.plot(filtered_sig_val[n_max_arg_partitioned])
    plt.plot(filtered_sig_val[n_max_arg_partitioned], "vr")
    plt.subplot(1, 3, 3)
    plt.plot(a3)
    plt.show()
    return np.flip(a3[n_max_sig_vals_sorted_index])

    ans = []
    print(f'len {len(sig_val)}')
    for i in range(n_max):
        best_val = float('-inf')
        best_ind = -1
        for idx, j in enumerate(sig_val):
            if req_range[0] <= sig[idx] <= req_range[1]:
                if best_val < j and (len(ans) == 0 or j < sig_val[ans[-1]]):
                    best_val = j
                    best_ind = idx
        if best_ind > -1:
            ans.append(best_ind)
    return ans


def get_min_max(dim, max_limit, min_limit):
    return max(min_limit, dim[0] - dim[1]), min(max_limit, dim[0] + dim[1])


def get_fft_sig(sig, time_step):
    # The FFT of the signal
    sig_fft = fftpack.fft(sig)

    # And the power (sig_fft is of complex dtype)
    power = np.abs(sig_fft) ** 2

    # The corresponding frequencies
    sample_freq = fftpack.fftfreq(sig.size, d=time_step)
    return sig_fft, power, sample_freq
