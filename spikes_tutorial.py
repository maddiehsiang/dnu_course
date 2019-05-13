
# Download http://data.cortexlab.net/singlePhase3/data/dataset.zip
# also download the 68-Gb .bin file from this link: http://data.cortexlab.net/singlePhase3/data

#%% setup for spike visualization and analysis
# Execute the following commands in Anaconda prompt (if Windows) or in terminal (if Mac):
# Do not include the #!
# conda create -y -n spikes_tutorial python=3.5
# conda activate spikes_tutorial
# conda install -y matplotlib pandas xarray numpy tqdm scipy spyder h5py requests joblib jupyter rise
# pip install spykes

#%% Setup for spikesorting (same procedure)
# conda create -y -n phy
# conda activate phy
# conda install -y pyqt=4 six numpy vispy click traitlets matplotlib scipy tqdm joblib h5py
# pip install phy phycontrib klusta cython


## Spike sorting  notes:
# make a backup of clusters.cvs with reference sort
## Notes
# conda great for beginners because can mess up and just start anew
# (make sure you keep the list of packages!)
# cross-platform
# doesnt matter which computer, bc so easy to set up

#TODO replace some of the code here with junk
#TODO test spyder
#TODO hubert and wiesel video - or is it another's?
#%%Import libraries
import matplotlib as mpl
mpl.use('Qt5Agg') # Do this if your plots are showing up in console and you can't zoom
import sys, matplotlib.pylab as plt, numpy as np,tqdm

#%% Import suppoorting code
# Insert your own path here!
sys.path.append('/Users/myroshnychenkm2/mmy/py/teaching/ukraine/')
import spikes_tutorial_dependencies as spike_deps
# Create pdf. We'll save all our results here (look ma no hands!)
pdf=spike_deps.make_report('/Users/myroshnychenkm2/Downloads/dataset/')

## First use of a library! Ctrl+click explanation

#%% Load spikes
neuron_ids, spike_times_all_neurons =spike_deps.load_spikes_from_phy('/Users/myroshnychenkm2/Downloads/dataset/')
#%%  visualize spiketimes ===============================================
#%% Let's inspect the spikes
print(neuron_ids)
print(spike_times_all_neurons)
#%% Let's inspect the timestamps from one neuron
id_of_interest=neuron_ids[0]
spike_times_of_interest=spike_times_all_neurons[neuron_ids == id_of_interest]
print(spike_times_of_interest)
plt.plot(spike_times_of_interest)
plt.title('Timestamps of neuron')
plt.ylabel('Time')
plt.xlabel('Number of spikes')
pdf.savefig()
# ============================ Q: Why is the curve progressively rising? ==================

#%%  visualize raster ===============================================
#%% Raster of one neuron, by hand
plt.clf()
plt.xlim([0, spike_times_of_interest.max()])
for this_timestamp in spike_times_of_interest[0:100]:
    plt.scatter(x=this_timestamp, y=1,marker='|',color='black')
    plt.show()
    plt.pause(.01)


#%% Raster of one, automatically
plt.scatter(x=spike_times_of_interest,
            y=np.ones(spike_times_of_interest.shape[0]),
            marker='|')
pdf.savefig()


#%% many units
plt.clf()
index_of_neuron=0
for this_id in np.unique(neuron_ids)[0:2]:
    print(this_id)
    spike_times_of_interest = spike_times_all_neurons[neuron_ids == this_id]
    index_of_neuron = index_of_neuron + 1 #OR index_of_neuron+=1
    for this_timestamp in spike_times_of_interest:
        plt.scatter(this_timestamp, index_of_neuron, marker='|', color='black')
        plt.show()
        plt.pause(.01)
pdf.savefig()
# Conclusion: with this basic building block, you can do anything! now go off and apply
#%% Automatic plot of all spikes together
plt.clf();plt.scatter(x=spike_times_all_neurons[spike_times_all_neurons<70],
                      y=neuron_ids[spike_times_all_neurons < 70], marker='|', c='k', alpha=.7)
pdf.savefig()
# Conclusion: with for loop as thebasic building block, you can do a lot!

#%% visualize binned raster ===============================================
#%% Difference vs binned raster
raster = spike_deps.bin_neurons(spike_times_all_neurons, neuron_ids, bin_size=.05)
print(raster) 
plt.clf()
raster.plot(robust=True)
#%% Convenient one-liners to "slice" the raster by time or neurons

raster.sel(Single_unit_id=160).plot()
raster.sel(Single_unit_id=160,Time=slice(0,50)).plot()
raster.sel(Single_unit_id=slice(20,1200),
           Time=slice(60,65)).plot(robust=True)
## Do you see the difference? We are missing-ish the up states
pdf.savefig()

#%%  PSTH
lfp, down_states = spike_deps.identify_down_states(spike_times_all_neurons)
#%% based on homemade code
raster = spike_deps.bin_neurons(spike_times_all_neurons, neuron_ids, bin_size=.005)
#%
psth=[]
for down_state in tqdm.tqdm(down_states):
    raster_now=raster.sel(Time=slice(down_state-.100,
                                     down_state+.300))
    psth.append(raster_now.sel(Single_unit_id=241).values[:80])

    # Note no equals sign
psth_all=np.vstack(psth)
# Conclusion: with for loop as thebasic building block, you can do anything!
## plot psth
plt.clf();plt.pcolormesh(psth_all)
## Q: What are the axes?


#%% ============= Kording psth toolbox ===============
psth_object = spike_deps.PSTH.make_psth(down_states)
spykes_df = spike_deps.PSTH.make_psth(down_states)
spykes_times = spike_deps.PSTH.spykes_get_times(spike_times_all_neurons, neuron_ids)
pop, all_psth = spike_deps.PSTH.spykes_summary(spikes=spykes_times, spykes_df=spykes_df, event='trialStart', window=[-300, 400], bin_size=5, plotose=True)
plt.figure();pop.plot_heat_map(all_psth, sortby='rate', sortorder='ascend', normalize=None, colors=['viridis'])  # or latency
## Note the periodicity
## Q: Do you think if you flip the detection, the result will be similar and opposite? Hint: Inspect the raster.
# Test your hypothesis by setting down_states = np.where(lfp > 90)[0]







