import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib as mpl

import pandas as pd

# data = pd.read_csv("")
geoData = gpd.read_file('usa.geojson')

# show the geoData
fig, ax = plt.subplots()
geoData.plot(ax=ax)

plt.show()
