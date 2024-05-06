import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.animation as animation
import matplotlib as mpl

import pandas as pd

data = pd.read_csv("combined_data.csv")
geo_data = gpd.read_file('usa.geojson')
avg_diff = pd.read_csv("avg_diff_data.csv")

# show the geo data
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.1, right=1, top=0.9)
geo_data.plot(ax=ax)

# create slider
ax_slider = plt.axes([0.1, 0.01, 0.8, 0.03])
slider = Slider(
    ax_slider,
    "Year",
    2002,
    2021,
    valinit=0,
    valstep=1,
)


def get_state_xy(state):
    return (
        geo_data[geo_data["State_Code"] == state].centroid.x,
        geo_data[geo_data["State_Code"] == state].centroid.y,
    )


fig.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(-10, 10), cmap='RdBu',),
             ax=ax, orientation='vertical', label='Percent Change in Acceptance Rate', pad=0.1)


def update_slider(val):
    target_year = slider.val

    ax.clear()

    # set the title on the top of the map
    ax.set_title(
        f"Average Change in Acceptance Rates for Universities from the {target_year - 1} to {target_year} Academic Year",
        fontsize=15,
        pad=20,
    )

    # set the slider value label to the year
    slider.valtext.set_text(target_year)

    # plot the map
    geo_data.plot(
        ax=ax,
        cmap='RdBu',
        edgecolor='gray',
        column=avg_diff[str(target_year)],
    )

    # remove axis labels
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    # update plot
    plt.draw()


slider.on_changed(update_slider)


def update_frame(frame):
    slider.set_val(frame)


# initial plotting
update_slider(2002)

# animate the plot
ani = animation.FuncAnimation(
    fig=fig,
    func=update_frame,
    frames=range(2002, 2022),
    interval=1000,
    repeat=True,
    repeat_delay=1000,
)

plt.show()

# save the animation
ani.save("acceptance_rate.gif", writer="pillow", fps=1)
