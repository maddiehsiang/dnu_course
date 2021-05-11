
# Raster of one neuron, by hand
for timestamp in spike_times_of_interest:
    plt.scatter(x=timestamp, y=1, marker='|', color='black')