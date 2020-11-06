# sound.py

from matplotlib import pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
import numpy as np

NOTE_FREQ = {
  'C': 261.6256,
  'D': 293.6648,
  'E': 329.6276,
  'F': 349.2282,
  'G': 391.9954
}

class SoundWave(object):
  """A class for working with digital audio signals."""

  def __init__(self, rate, samples):
    """Set the SoundWave class attributes.

    Parameters:
      rate (int): The sample rate of the sound.
      samples ((n,) ndarray): NumPy array of samples.
    """
    # Store params as attributes
    self.rate = rate
    self.samples = samples

  def plot(self, show_dft=False):
    """Plot the graph of the sound wave (time versus amplitude)."""
    fig, ax = plt.subplots(2, figsize=(10, 6))
    plt.subplots_adjust(hspace = 0.4)
    
    # Adjust figure
    ax[0].set_ylim(bottom=(-1)*32768, top=32767)
    ax[0].set_xlabel("Time (seconds)")
    ax[0].set_ylabel("Samples")
    
    # Adjust for seconds on the x axis
    seconds = len(self.samples) / self.rate
    time = np.linspace(0, seconds, len(self.samples))
    
    # Plot samples
    ax[0].plot(time, self.samples)
    
    if (show_dft):
      dft = fft(self.samples)
      ax[1].set_xlabel("Frequency (Hz)")
      ax[1].set_ylabel("Magnitude")
      x = np.linspace(0, len(self.samples), len(dft)) * (self.rate / len(self.samples))
      ax[1].plot(x[:len(x)//2], np.abs(dft[:len(x)//2]))
      
    else:
      ax[1].set_visible(False)
    
    plt.show()

  def export(self, filename, force=False):
    """Generate a wav file from the sample rate and samples. 
    If the array of samples is not of type np.int16, scale it before exporting.

    Parameters:
      filename (str): The name of the wav file to export the sound to.
    """
    samples = self.samples
    
    # Check if scaling is needed
    if (self.samples.dtype != np.int16) or force:     
      samples = samples / abs(samples).max()
      samples *= 32767
      samples = samples.real
      samples = samples.astype(np.int16)
    
    # Write out
    wavfile.write(filename, self.rate, samples)
    
  def __add__(self, other):
    """Combine the samples from two SoundWave objects.

    Parameters:
      other (SoundWave): An object containing the samples to add
        to the samples contained in this object.
    
    Returns:
      (SoundWave): A new SoundWave instance with the combined samples.

    Raises:
      ValueError: if the two sample arrays are not the same length.
    """
    # Check that addition is valid
    if (len(self.samples) != len(other.samples)):
      raise ValueError("SoundWaves are not the same length")
      
    # Add sampels elementwise
    sum_samples = self.samples + other.samples
    
    return SoundWave(self.rate, sum_samples)
    
  def __rshift__(self, other):
    """Concatentate the samples from two SoundWave objects.

    Parameters:
      other (SoundWave): An object containing the samples to concatenate
        to the samples contained in this object.

    Raises:
      ValueError: if the two sample rates are not equal.
    """
    # Check if shift is valid
    if (self.rate != other.rate):
      raise ValueError("SoundWaves have different sample rates")
    
    shift_samples = np.concatenate((self.samples, other.samples))
    
    return SoundWave(self.rate, shift_samples)

  def __mul__(self, other):
    """Convolve the samples from two SoundWave objects using circular convolution.
    
    Parameters:
      other (SoundWave): An object containing the samples to convolve
        with the samples contained in this object.
    
    Returns:
      (SoundWave): A new SoundWave instance with the convolved samples.

    Raises:
      ValueError: if the two sample rates are not equal.
    """
    # Check the rates
    if (self.rate != other.rate):
      raise ValueError("The sample rates do not match. Must be the same.")
    
    # Check the samples
    f = self.samples
    g = other.samples
    f = np.pad(f, (0, abs(len(g) - len(f))), 'constant')
    g = np.pad(g, (0, abs(len(f) - len(g))), 'constant')
         
    conv = ifft(np.multiply(fft(f), fft(g)))
         
    return SoundWave(self.rate, conv)

  def __pow__(self, other):
    """Convolve the samples from two SoundWave objects using linear convolution.
    
    Parameters:
      other (SoundWave): An object containing the samples to convolve
        with the samples contained in this object.
    
    Returns:
      (SoundWave): A new SoundWave instance with the convolved samples.

    Raises:
      ValueError: if the two sample rates are not equal.
    """
    # Check the rates
    if (self.rate != other.rate):
      raise ValueError("The sample rates do not match. Must be the same.")
      
    # Check the sample lengths
    f = self.samples
    g = other.samples
    m = len(f)
    n = len(g)
    
    a = int(np.ceil(np.log2(n + m - 1)))
    
    f = np.pad(f, (0, (2**a) - m), 'constant')
    g = np.pad(g, (0, (2**a) - n), 'constant')
    
    conv = ifft(np.multiply(fft(f), fft(g)))
    
    return SoundWave(self.rate, conv[:m + n - 1])

  def clean(self, low_freq, high_freq):
    """Remove a range of frequencies from the samples using the DFT. 

    Parameters:
      low_freq (float): Lower bound of the frequency range to zero out.
      high_freq (float): Higher boound of the frequency range to zero out.
    """
    k_low = int(low_freq * (len(self.samples) / self.rate))
    k_high = int(high_freq * (len(self.samples) / self.rate))
    
    dft = fft(self.samples)
    n = len(dft)
    
    dft[k_low:k_high] = 0
    dft[n - k_high:n - k_low] = 0
    
    clean = ifft(dft)
    
    self.samples = clean

# end class SoundWave


def audio_sequence(note_sequence, duration=1):
  """Generate an instance of the SoundWave class corresponding to 
  the desired soundwave. Uses sample rate of 44100 Hz.
  
  Parameters:
      note_sequence (list(str)): The note values to generate.
      duration (float): The length of the desired sound per note in seconds.
  
  Returns:
      sound (SoundWave): An instance of the SoundWave class.
  """
  if len(note_sequence) == 0:
    raise ValueError('Cannot generate audio for empty note sequence')

  hertz = [NOTE_FREQ[note] for note in note_sequence]

  audio = generate_note(hertz[0], duration)

  # Add the shifting of the other notes in the note_sequence
  for freq in hertz[1:]:
    audio = audio >> generate_note(freq, duration)

  return audio

def generate_note(frequency, duration=1):
  """Generate an instance of the SoundWave class corresponding to 
  the desired soundwave. Uses sample rate of 44100 Hz.
  
  Parameters:
      frequency (float): The frequency of the desired sound.
      duration (float): The length of the desired sound in seconds.
  
  Returns:
      sound (SoundWave): An instance of the SoundWave class.
  """
  # Sample rate and number of samples
  rate = 44100
  N = rate * duration
  
  # Get sample
  x = np.linspace(0, duration, N)
  samples = np.sin(2 * np.pi * x * frequency)
  
  note = SoundWave(rate, samples)
  
  return note
