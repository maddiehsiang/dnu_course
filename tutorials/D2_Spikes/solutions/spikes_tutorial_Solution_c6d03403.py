def half_a_second(raster, timestamp):
    return raster.sel(Time=slice(timestamp - .250,
                                 timestamp + .250)).values[:50]


peth = [half_a_second(raster241, timestamp) for timestamp in event_times]
p2th = np.vstack(peth)

plt.pcolormesh(peth);