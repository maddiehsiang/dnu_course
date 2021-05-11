def half_a_second(raster, timestamp):
    return raster.sel(Time=slice(timestamp - .250,
                                 timestamp + .250)).values[:50]


psth = [half_a_second(raster241, timestamp) for timestamp in down_states]
psth = np.vstack(psth)

plt.pcolormesh(psth);