# Whole raster for one neuron, no loop
plt.scatter(x=spike_times_of_interest,
            y=np.ones(spike_times_of_interest.shape[0]),
            marker='|', color='black');