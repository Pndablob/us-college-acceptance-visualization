import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib as mpl

import pandas as pd

data = pd.read_csv("MathMCASHampshireCountyCleaned.csv")
geoData = gpd.read_file('hampshire_county.json')

# show the geoData
fig, ax = plt.subplots()
geoData.plot(ax=ax)

# create slider
slider_years = [2019, 2021, 2022, 2023]
axSlider = plt.axes([0.1, 0.01, 0.8, 0.03])
slider = Slider(
    axSlider,
    "Year",
    0,
    len(slider_years) - 1,
    valinit=0,
    valstep=1,
)


def getXYFromName(name):
    return (
        geoData[geoData["DISTRICT_N"] == name].centroid.x,
        geoData[geoData["DISTRICT_N"] == name].centroid.y,
    )


def getColorFromPercent(percent):
    # reds
    # scl = [
    #     [0.0, "#ffffff"],
    #     [0.2, "#fdcab5"],
    #     [0.4, "#fc8b6b"],
    #     [0.6, "#f14432"],
    #     [0.8, "#bd151a"],
    #     [1.0, "#62000c"],
    # ]

    # greens
    # scl = [
    #     [0.0, "#ffffff"],
    #     [0.2, "#d4eece"],
    #     [0.4, "#96d492"],
    #     [0.6, "#4aaf61"],
    #     [0.8, "#157f3b"],
    #     [1.0, "#00461c"],
    # ]

    # blues
    scl = [
        [0.0, "#ffffff"],
        [0.2, "#d0e1f2"],
        [0.4, "#94c4df"],
        [0.6, "#4997c9"],
        [0.8, "#1663aa"],
        [1.0, "#08316d"],
    ]

    for i in range(len(scl)):
        if percent <= scl[i][0]:
            return scl[i][1]
    return scl[-1][1]


fig.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0, 100), cmap='Blues'),
             ax=ax, orientation='vertical', label='Percentage')

def update(val):
    yearTarget = slider_years[int(slider.val)]

    if yearTarget == 2020:
        return

    ax.clear()

    # set the title on the top of the map
    ax.set_title(
        f"Percentage of 10th Grade Students in Hampshire County Meeting and Exceeding Expectations on the {yearTarget} Math MCAS",
        fontsize=15,
        pad=20,
    )

    # set the slider value label to the year
    slider.valtext.set_text(yearTarget)

    # for each section in the county, print the name + the "Meeting and Exceeding Expectations Percent"
    for year, name, percent in zip(
            data["Year"],
            data["District Name"],
            data["Meeting and Exceeding Expectations Percent"],
    ):
        if year != yearTarget:
            continue

        display_name = "South\nHadley" if name == 'South Hadley' else name

        x, y = getXYFromName(name)
        ax.text(
            x+400 if name == 'Easthampton' else x,
            y,
            display_name,
            fontsize=9,
            ha='center',
        )

        # update the color of the district based on the percent
        geoData[geoData["DISTRICT_N"] == name].plot(
            ax=ax,
            color=getColorFromPercent(percent),
        )

        # set polygon boarder
        geoData[geoData["DISTRICT_N"] == name].boundary.plot(
            ax=ax,
            color="#3c3c3c",
        )

    # remove axis
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    # update plot
    plt.draw()


slider.on_changed(update)

# initial plotting
update(2019)

plt.show()
