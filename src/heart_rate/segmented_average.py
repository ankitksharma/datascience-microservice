import numpy as np
from scipy.signal import find_peaks
import scipy.fftpack as fftpack
import math


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
    while True:
        bucket = y2[int(bucket_i * bucket_size_secs * fps): int(
            (bucket_i + 1) * bucket_size_secs * fps)]  # use decay weights
        if bucket.shape[0] <= 0: break
        sig_fft, power, sample_freq = get_fft_sig(bucket, 1 / fps)
        max_fq_arr = find_max_frequencies_within_range(power, sample_freq, freq_limits, 2)
        max_fq, min_fq = max(max_fq_arr), min(max_fq_arr)
        max_fq_mean = np.mean(max_fq_arr) if abs(max_fq - min_fq) * 60 <= max_bpm_diff_for_mean else max_fq
        if not math.isnan(max_fq_mean):
            sum_max_freq += max_fq_mean
        bucket_i += 1
        peaks2, _ = find_peaks(bucket, distance=7.5, prominence=2)  # BEST!
        max_bps = max(max_bps, peaks2.shape[0] * fps / bucket.shape[0])
        min_bps = min(min_bps, peaks2.shape[0] * fps / bucket.shape[0])
        bucket_bps = peaks2.shape[0] * fps / (bucket.shape[0])
        print(f'{bucket_i} {bucket_bps * 60} {max_fq_arr * 60} {sum_max_freq * 60}')
        sum_avg_bps += bucket_bps
    avg_max_freq = sum_max_freq / bucket_i
    return avg_max_freq * 60


def get_max_power_frequencies(bucket, fps, freq_limits):
    sig_fft, power, sample_freq = get_fft_sig(bucket, 1 / fps)
    return find_max_frequencies_within_range(power, sample_freq, freq_limits, 2)


# returns freq for n_max power values in the req_range and in decreasing order
def find_max_frequencies_within_range(powers, frequencies, req_range, n_max):
    # filtered based on sig range
    filtered_freq, filtered_power = filter_on_frequency_range(frequencies, powers, req_range)

    # indices for n_max values
    n_max_power_indices = filter_on_power_k_order_statistic(filtered_power, n_max)

    # indices order required to sort filtered_n_max_sig_vals (sort order is increasing)
    increasing_filtered_sig_val_indices = np.argsort(filtered_power[n_max_power_indices])

    # frequencies for the n_max power within range
    filtered_n_max_frequency = filtered_freq[n_max_power_indices]

    # return in decreasing order of power
    return np.flip(filtered_n_max_frequency[increasing_filtered_sig_val_indices])


# returns filtered_sig, and filtered_sig_val based on the sig_val range
def filter_on_frequency_range(frequencies, powers, req_range):
    filtered_freq_indices = np.logical_and(frequencies >= req_range[0], frequencies <= req_range[1])
    return frequencies[filtered_freq_indices], powers[filtered_freq_indices]


def filter_on_power_k_order_statistic(power, n_max):
    return np.argpartition(power, -n_max)[-n_max:]


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
