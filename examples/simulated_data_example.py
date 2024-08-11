# simulates random data and visulizes results
import numpy as np
from QPPython import find_qpp

'''
Create simulated data
'''
npt = 10 # number of qpp template timepoints, qpp template window size
nX = 120 # number of features/channels/voxels
nT = 450 # number of total timepoints

data = np.random.rand(nX, nT)

# get random starting qpp template from the data
random_starting_point = np.random.randint(0,nT-npt)
print('Started with qpp template at: ',random_starting_point)
T = data[:,random_starting_point:random_starting_point+npt]

qpp_pattern, cn = find_qpp(data,T)
peaks, _ = find_peaks(cn)

'''
plot the qpp similarity/convolution timeseries
'''
fig, axs = plt.subplots(figsize=(12,4))
fig.suptitle('QPP Timeseries and Peaks')
axs.plot(cn)
for peak in peaks:
  axs.axvline(x=peak,alpha=.5,c='orange')
  
axs.axvline(x=random_starting_point,alpha=1,c='red',label='Initial QPP')
axs.axvline(x=random_starting_point+npt,alpha=1,c='red')
axs.legend()

'''
plot the qpp pattern
'''
fig, axs = plt.subplots(1,3,figsize=(12,5),width_ratios=(3,1,1))

axs[0].set_title('Data')
axs[0].imshow(data,aspect='auto')
axs[0].axvline(x=random_starting_point,c='red',label='First QPP')
axs[0].axvline(x=random_starting_point+npt,c='red')
axs[0].legend()

axs[1].set_title('First QPP')
axs[1].imshow(T)

axs[2].set_title('Final QPP')
axs[2].imshow(qpp_pattern)
