import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import matplotlib.colors as mcolors
import numpy as np
import os

def gridlines(ax):
    gl = ax.gridlines(draw_labels=True, zorder=100, linestyle='dashed', alpha=0.5,
                     color='#383838', lw=0.25)
    gl.xlocator = mpl.ticker.FixedLocator(range(-180, 181, 20))  # Add latitude grid lines every 30 degrees
    gl.ylocator = mpl.ticker.FixedLocator(range(-90, 91, 10))  # Add longitude grid lines every 20 degrees
    gl.right_labels = False  # Display longitude labels on the left side
    gl.top_labels = False  # Display latitude labels at the bottom
    gl.xlabel_style = {'size': 12, 'color': '#383838'}
    gl.ylabel_style = {'size': 12, 'color': '#383838', 'rotation': 45}

def plot_tracks(tracks):
    fig = plt.figure(figsize=(14.5, 10))
    datacrs = ccrs.PlateCarree()

    # Plot the tracks
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([-180, 180, -90, 90], ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)

    # Add gridlines
    gridlines(ax)

    # Plot the tracks
    ax.plot(tracks['lon vor'], tracks['lat vor'], color='#383838', linewidth=0.5, transform=datacrs)

    plt.show()
