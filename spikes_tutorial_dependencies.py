import os

import matplotlib.pylab as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
import xarray as xr
from matplotlib.backends.backend_pdf import PdfPages


def make_report(path_to_pdf):
    """
    Makes a pdf report. Example:
    pdf = make_report() #Make pdf.
    # plot something....
    pdf.savefig() # Save new figures to it using:
    pdf.close() # finalize

    :param path_to_pdf:
    :return: pdf object
    """
    return PdfPages(path_to_pdf + '/' + 'report.pdf')


def load_spikes_from_phy(path_to_data='/Users/myroshnychenkm2/Downloads/dataset/', sampling_frequency=30000):
    """
    Get spikes from a kilosort/phy result folder
    :param path_to_data:
    :param sampling_frequency:
    :return: 
    :id: neuron id, 1xN
    :ts: corresponding spiketime, 1xN
    """
    groupfname = os.path.join(path_to_data, 'cluster_groups.csv')
    groups = pd.read_csv(groupfname, delimiter='\t')

    # load spike times and cluster IDs
    with open(path_to_data + 'spike_clusters.npy', 'rb') as f:
        ids = np.load(f).flatten()
    with open(path_to_data + 'spike_times.npy', 'rb') as f:
        ts = np.load(f).flatten()

    # Create the list of our "good" labeled units
    ids_to_take = groups[(groups.group == 'good')].cluster_id
    # Find which spikes beloing to our "good" groups
    spikes_to_take = []
    for i in tqdm(ids_to_take, desc='Selecting only good spikes'):
        spikes_to_take.extend((ids == i).nonzero()[0])
    # only take spikes that are in our list
    ids = np.array(ids[spikes_to_take])
    ts = np.array(ts[spikes_to_take]).astype(float) / sampling_frequency

    return ids, ts


def bin_neuron(spike_times, bin_size=.100, window=None):
    """
    Make binned raster for a single neuron
    :param spike_times:
    :param bin_size: in sec
    :param window:
    :return:
    """
    if window is None:
        window = [0, spike_times.max()]
    bins = np.arange(window[0], window[1] + bin_size, bin_size)
    return np.histogram(spike_times, bins)[0]


def bin_neurons(spike_times, neuron_ids, bin_size=None, window=None, plotose=False):
    """
    Make binned raster for many neurons
    :param spike_times:
    :param neuron_ids:
    :param bin_size: in sec
    :param window:
    :param plotose:
    :return:
    """
    if window is None:
        window = [0, spike_times.max()]
    # the following uses an inline for loop (look it up):
    spike_counts = [bin_neuron(spike_times[neuron_ids == neuron_id], bin_size, window)
                    for neuron_id in tqdm(np.unique(neuron_ids))]
    spike_counts = np.vstack(spike_counts)
    raster = xr.DataArray(spike_counts, coords=dict(Time=np.arange(window[0], window[1] + bin_size, bin_size)[:-1],
                                                    Single_unit_id=range(len(np.unique(neuron_ids)))),
                          dims=['Single_unit_id', 'Time'])
    if plotose:
        raster.plot(robust=True)
    return raster


def identify_down_states(ts, bin_size=.05, number_of_neurons_treshold=20, minimum_time_between_states=0.15):
    """
    Find spontaneous periods of quiecence in spiketimes
    :param ts:
    :param bin_size:
    :param number_of_neurons_treshold:
    :param minimum_time_between_states:
    :return:
    """
    lfp = bin_neuron(np.sort(ts), bin_size=bin_size)
    down_states = np.where(lfp < number_of_neurons_treshold)[0]
    down_states_lengths = np.diff(down_states)
    print(f'Eliminating {down_states[1:][down_states_lengths < .15 / bin_size].shape} that are too short')
    down_states = down_states[1:][down_states_lengths > minimum_time_between_states / bin_size]
    print(f'Ended up with {down_states.shape} down states')
    # convert into seconds:
    down_states = down_states * bin_size
    down_states -= .03
    print(down_states[(down_states > 63) & (down_states < 68)])  # compare with raster
    return lfp, down_states


class PSTH:
    """
    A collection of functions dealing with peristimulus time histogram
    """

    @staticmethod
    def make_psth(trial_starts):
        """
        Simple wrapper creating a dataframe with times we want to lock onto
        :param trial_starts: List of times of interest (trials)
        :return: spykes object
        """
        trials = pd.DataFrame()
        trials['trialStart'] = trial_starts
        return trials

    @staticmethod
    def spykes_get_times(s_ts, s_id, debug=False):
        """
        Use spykes library
        :param s_ts:
        :param s_id:
        :param debug:
        :return:
        """

        def print_spyke(spykess):
            [print(len(spykess[i].spiketimes)) for i in range(len(spykess))]

        from spykes.plot import neurovis
        s_id = s_id.astype('int')
        neuron_list = list()
        for iu in np.unique(s_id):
            spike_times = s_ts[s_id == iu]
            if len(spike_times) < 2:
                if debug:
                    print('Too few spiketimes in this unit: ' + str(spike_times))
                else:
                    pass  # neuron_list.append(NeuroVis([],'ram'+str(iu)))
            else:
                neuron = neurovis.NeuroVis(spike_times, name='ram' + str(iu))
                neuron_list.append(neuron)

        if debug:
            print_spyke(neuron_list)
        return neuron_list

    @staticmethod
    def spykes_summary(spikes, spykes_df, event, window=[-100, 100], bin_size=10, fr_thr=.1, plotose=True):
        """

        :param spikes:
        :param spykes_df:
        :param event:
        :param window:
        :param bin_size:
        :param fr_thr:
        :param plotose:
        :return:
        """
        import spykes
        assert window[1] - window[0] > 0, 'Window size must be greater than zero!'
        # filter firing rate
        spikes = [i for i in spikes if i.firingrate > fr_thr]
        pop = spykes.plot.popvis.PopVis(spikes)
        # calculate psth
        mean_psth = pop.get_all_psth(event=event, df=spykes_df, window=window, binsize=bin_size, plot=False)
        assert mean_psth['data'][0].size > 0, 'Empty group PSTH!'
        if plotose:
            # % plot heatmap of average psth
            _ = plt.figure(figsize=(10, 10))
            #        fig.subplots_adjust(hspace=.3)
            # set_trace()
            pop.plot_heat_map(mean_psth, sortby=None, sortorder='ascend', normalize=None,
                              colors=['viridis'])  # or latency

            # %% Population PSTH
            plt.figure()
            pop.plot_population_psth(all_psth=mean_psth, event_name='Event',
                                     colors=([.5, .5, .5], [0, .6, 0]))

        return pop, mean_psth
