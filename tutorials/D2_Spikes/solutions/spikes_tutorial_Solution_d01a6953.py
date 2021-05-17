## Bin whole dataset:
raster_huge = bin_neurons(spike_times_all_neurons_huge, neuron_ids_huge, bin_size=.05)

## Plot selection:
raster_huge.sel(Neuron_ID=slice(20, 1200),
                Time=slice(60, 65)
                ).plot(robust=True);