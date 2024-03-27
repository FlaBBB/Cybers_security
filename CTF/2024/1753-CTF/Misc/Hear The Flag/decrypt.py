from itertools import permutations

import numpy as np
from Crypto.Util.number import long_to_bytes
from scipy.fft import *
from scipy.io import wavfile
import matplotlib.pyplot as plt

sr, data = wavfile.read("./flag-sound [bass].wav")


def freq(start_time, end_time):
    global data
    # Open the file and convert to mono
    if data.ndim > 1:
        data = data[:, 0]
    else:
        pass

    # Return a slice of the data from start_time to end_time
    dataToRead = data[int(start_time * sr / 1000) : int(end_time * sr / 1000)]

    # Fourier Transform
    N = len(dataToRead)
    yf = rfft(dataToRead)
    xf = rfftfreq(N, 1 / sr)

    # Uncomment these to see the frequency spectrum as a plot
    plt.plot(xf, np.abs(yf))
    plt.show()

    # Get the most dominant frequency and return it
    idx = np.argmax(np.abs(yf))
    freq = xf[idx]
    return freq


print(freq(9000,10000))

# i = 60
# step = 1248
# freqs = []
# message = []
# while i < 64800:
#     if i + step < 64800:
#         f = round(i, i + step)
#         if f not in freqs and f + 1 not in freqs and f - 1 not in freqs:
#             freqs.append(f)
#         message.append(f)
#         i += step
#     else:
#         break
# print(freqs)

# for freqs in permutations(freqs, 7):
#     res = ""
#     for m in message:
#         min_idx = len(freqs)
#         min_diff = 100
#         for i, f in enumerate(freqs):
#             diff = abs(m - f)
#             if diff < min_diff:
#                 min_diff = diff
#                 min_idx = i
#         res += str(min_idx)

#     res = res[::-1]
#     num = 0
#     for i, digit in enumerate(res):
#         num += int(digit) * 7**i

#     print(long_to_bytes(num))
