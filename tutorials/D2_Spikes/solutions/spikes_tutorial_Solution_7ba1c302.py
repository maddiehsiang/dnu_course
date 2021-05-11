
# Make a 3d plot with mean PSTH for all neurons
raster_object.plot_heat_map(all_psth, sortby='rate', sortorder='ascend', normalize=None, colors=['viridis'])  # or latency