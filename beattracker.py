#!/usr/bin/env python
#Script to test beattracking in music

#http://nbviewer.ipython.org/github/bmcfee/librosa/blob/master/examples/LibROSA%20demo.ipynb
# Install: https://github.com/bmcfee/librosa


# We'll need numpy for some mathematical operations
import numpy as np
import librosa # Librosa for audio
import matplotlib.pyplot as plt # matplotlib for displaying the output
#matplotlib inline

# And seaborn to make it look nice
import seaborn
seaborn.set(style='ticks')
import IPython.display  # and IPython.display for audio output

#Test Audio File
audio_path = librosa.util.example_audio_file()

#audio_path = '/path/to/your/favorite/song.mp3'
y, sr = librosa.load(audio_path)

#librosa.load(audio_path, sr=44100) #Sample 22050Hz Default

#Ensure samplerate script works correctly.
print 'HAS_SAMPLERATE: ', librosa.core.audio._HAS_SAMPLERATE

# Now, let's run the beat tracker.
plt.figure(figsize=(12, 6))
tempo, beats = librosa.beat.beat_track(y=y_percussive, sr=sr)

# Let's re-draw the spectrogram, but this time, overlay the detected beats
plt.figure(figsize=(12,4))
librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')

# Let's draw transparent lines over the beat frames
plt.vlines(beats, 0, log_S.shape[0], colors='r', linestyles='-', linewidth=2, alpha=0.5)

plt.axis('tight')

plt.colorbar(format='%+02.0f dB')

plt.tight_layout()
