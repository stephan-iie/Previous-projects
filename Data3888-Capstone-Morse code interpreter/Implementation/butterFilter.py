from scipy import signal

def butterFilter(sig):
    fs = 1000
    fc = 2 # Cut-off frequency of the filter
    w = fc / (fs / 2) # Normalize the frequency
    b, a = signal.butter(4, w, 'low')
    output = signal.filtfilt(b, a, sig)
    return output

def notchFilter(data):
  # Create/view notch filter
  samp_freq = 10000  # Sample frequency (Hz)
  notch_freq = 50.0  # Frequency to be removed from signal (Hz)
  quality_factor = 0.1 # Quality factor
  b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)
  freq, h = signal.freqz(b_notch, a_notch, fs = samp_freq)

  # apply notch filter to signal
  y_notched = signal.filtfilt(b_notch, a_notch, data)

  # 'A T T E N U A T E D' Data
  y_notched = (y_notched - 510)*15
  #plt.plot(y_notched)
  return y_notched