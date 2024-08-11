import numpy as np
from tqdm import tqdm
from scipy.signal import find_peaks
#import matplotlib.pyplot as plt
#from scipy.stats import zscore


def find_qpp(data,T):

  '''
  Given a timeseries data and a qpp template this function calculates 
  Quasi-Periodic Pattens defined in this paper: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10557593/ 

  Data can be in any modality and scale,
  QPP template can have any lenght, and its lenght will determine the lenght of the returned qpp convolution timeseries

  Will return the found qpp pattern and a timeseries of its match to the inputted timeseries data.
  
  Arguments:
    data {ndarray} -- 2d numpy array of shape (# of features/channels/voxels, # of timepoints) that stores timeseries data
    T {ndarray} -- 2d numpy array of shape (# of features/channels/voxels, # of timepoints in QPP window) that stores the initially inputed QPP pattern.
  Returns:
    qpp {ndarray} -- 2d numpy array of shape (# of features/channels/voxels, # of timepoints in QPP window) that stores the resulting QPP pattern.
    cn {ndarray} -- 1d numpy array of shape (# of timepoints - qpp template window size) 
        stores the final convolution timeseries i.e. the qpp similarity timeseries. It is the normalized version of the template convolution timeseries
    
  '''
  qpp_window_size = T.shape[1]
  ns = data.shape[1]- qpp_window_size # ns is the number of extractable windows in the data
  nX = data.shape[0] # nX is the number of timepoints in the data
  
  # initialize a random qpp similarity timeseries to compare with the first iteration of the loop.
  # (there probably is a more graceful way to do this, show me how please)
  # also c will be the 1d numpy array that stores the convolution timeseries i.e. the qpp similarity timeseries
  initial_random_c = np.random.rand(ns)

  # set the qpp pattern variable to the one inputted
  new_pattern = T

  # initialize a tqdm progress bar
  pbar = tqdm()

  # while the difference between the last and the current qpp convolution timeseries is smaller than 0.9999
  while qpp_similarity_to_last < 0.9999:

    # initialize c to store resulting convolution timeseries
    c = np.zeros(ns)

    # iterate over time with a sliding window
    for start in range(ns):
        end = start + qpp_window_size
        window = data[:, start:end]
        # its not clear if the normalisation happens PER window, or before segmenting the windows
        #normalized_window = zscore(window,axis=0) # over voxels axis

        # perform the convolution
        c[start] = np.sum(window * new_pattern)

    # normalize the convolution timeseries
    c_mean = np.mean(c)
    c_std = np.std(c)
    cn = (c - c_mean) / c_std

    # find peaks to use as indices to create a new avearge qpp pattern
    peaks, _ = find_peaks(cn)

    # update the qpp pattern based on peaks
    # instead of starting from zeros, could also directly add to the current qpp template
    # by commenting the line below:
    new_pattern = np.zeros_like(T)

    for peak in peaks:
      peak_pattern = data[:,peak:peak+npt]
      new_pattern += peak_pattern
    new_pattern = new_pattern/peaks.shape[0]

    # update the progress bar
    pbar.update(1)

    # update the while loop variables
    qpp_similarity_to_last = np.corrcoef(cn, last_c)[0][1]
    last_c = cn
    qpp = new_pattern
    '''
    Should you want to, you can plot a summary figure for each iteration for exploration/troubleshooting

    fig, axs = plt.subplots(1,3,figsize=(5,2),width_ratios=(3,1,1))

    axs[0].imshow(data,aspect='auto')
    axs[0].axvline(x=random_starting_point,c='red')
    axs[0].axvline(x=random_starting_point+npt,c='red')

    axs[1].imshow(T)
    axs[2].imshow(new_pattern)
    '''
  pbar.close()
  return qpp, cn
