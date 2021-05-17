
# make a peth object using the provided Spykes toolbox:
events = PETH.events(event_times)

# make a list of spiketimes that our toolbox can understand:
spikes = PETH.spykes_get_times(spike_times_all_neurons_huge,
                               neuron_ids_huge)
# Get mean PETH for all neurons
raster_object, all_psth = PETH.spykes_summary(spikes=spikes,
                                              events=events,
                                              window=[-300, 400],
                                              bin_size=5,
                                              plotose=True)