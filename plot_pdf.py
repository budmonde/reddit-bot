import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from character_distribution import *

import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors

### Plots formatting ###

font = {'family': 'serif',
        'weight': 'normal',
        'size': 14}
plt.rc('font', **font)
plt.rc('lines', linewidth=2)

def get_cmap(N):
    '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct 
    RGB color.'''
    color_norm  = colors.Normalize(vmin=0, vmax=N-1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='seismic') 
    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    return map_index_to_rgb_color

def plot_pdf(arr_of_arr, label):
  N = 15
  cmap = get_cmap(N)
  ii = 0
  for arr in arr_of_arr:
    labels = [i[0] for i in arr]
    probs = [i[1] for i in arr]
    x = np.arange(len(arr))
    if ii == 5:
      plt.plot(x, probs, marker=".", lw=1, color='b', label=label[ii])
    else:
      plt.plot(x, probs, marker=".", lw=1, color=cmap(9 + ii), label=label[ii])
    plt.xticks(x, labels)
    #plt.fill_between(x, 0, probs, color=c[ii], alpha=0.5)
    ii += 1
  plt.title("Character probability: LSTM (hs size: 512, layers: 3")
  plt.ylabel("Probability")
  plt.xlabel("Character")
  plt.legend(loc=1)
  plt.tight_layout()
  plt.show()
  


if __name__ == "__main__":
  thres = int(sys.argv[1])
  arr_of_arr = []
  label = []
  dr = "lstm_train"
  arr_of_arr.append(text_sorted_char_dist(dr+"/sample03.70.txt", thres))
  label.append("Epoch 03.70")
  arr_of_arr.append(text_sorted_char_dist(dr+"/sample11.11.txt", thres))
  label.append("Epoch 11.11")
  arr_of_arr.append(text_sorted_char_dist(dr+"/sample29.63.txt", thres))
  label.append("Epoch 29.63")
  arr_of_arr.append(text_sorted_char_dist(dr+"/sample40.74.txt", thres))
  label.append("Epoch 40.74")
  arr_of_arr.append(text_sorted_char_dist(dr+"/sample50.00.txt", thres))
  label.append("Epoch 50.00")
  arr_of_arr.append(text_sorted_char_dist("4qo3ia.txt", thres))#[1:])
  label.append("Baseline")
  plot_pdf(arr_of_arr, label)
