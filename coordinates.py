import numpy as np
from scipy.fft import fft

def loading_fourier_data(audio):
 
    sub_buffer_fourier_data = fft(audio)
    return sub_buffer_fourier_data


def audio_to_coordinates(audio):
    new = []
    for i in range(len(audio)):
        x =  i * 10
        y = abs(audio[i])
        new.extend([x,y])
    return np.array(new,dtype=np.float32)


def normalize_coordinates(coordinates,RESOLUTION):
    x = len(coordinates) //2
    new = []
    for i in range(x):
        if (i+1)%2 == 1:
            new.append((coordinates[i]/(2.5 * x) - 0.5) * 2)
        else:
            new.append((coordinates[i]/100 - 0.5) * 2)
    return np.array(new,dtype=np.float32)
    
    
    
