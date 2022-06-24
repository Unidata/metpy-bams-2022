# %% [markdown]
# # Figure 3
# ## Using `cross_section` to sample data along a great circle slice.
# Adapted from https://unidata.github.io/MetPy/v1.3/examples/cross_section.html.


# %%
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib import rcParams
from matplotlib.patheffects import withStroke

import metpy.calc as mpcalc

# get_test_data is used for internal MetPy testing and not supported publicly
from metpy.cbook import get_test_data
from metpy.interpolate import cross_section, log_interpolate_1d

# %% [markdown]
# We update plot font sizes for final figure legibility.

# %%
label_sizes = {"xtick.labelsize": 12, "ytick.labelsize": 12, "axes.labelsize": 14}
rcParams.update(label_sizes)

# %% [markdown]
# Read NARR data valid 1800 UTC 4 April 1987, provided as part of MetPy's internal testing data.

# %%
data = xr.open_dataset(get_test_data("narr_example.nc", False))
data = data.metpy.parse_cf().squeeze()

# %%
topo = xr.open_dataset("../hgt.sfc.nc")
topo = topo.metpy.parse_cf("hgt").squeeze()

# %% [markdown]
# Define endpoints for cross section and calculate cross sections for for data and corresponding topography.

# %%
start = (37.0, -105.0)
end = (35.5, -65.0)

topo_cross = cross_section(topo, start, end)
cross = cross_section(data, start, end).set_coords(("lat", "lon"))


# %% [markdown]
# Produce calculations along plane of cross section

# %%
c = []
for index in cross.index:
    a = cross["Geopotential_height"].sel(index=index)
    b = topo_cross.sel(index=index)
    c.append(log_interpolate_1d(b, a, a.metpy.vertical))

da = xr.DataArray(
    np.array(c).squeeze(), coords=topo_cross.coords, dims="index", attrs={"units": c[0].units}
)

cross["topo_pressure"] = da

# %%
cross["Potential_temperature"] = mpcalc.potential_temperature(
    cross["isobaric"], cross["Temperature"]
)
cross["Relative_humidity"] = mpcalc.relative_humidity_from_specific_humidity(
    cross["isobaric"], cross["Temperature"], cross["Specific_humidity"]
)
cross["u_wind"] = cross["u_wind"].metpy.convert_units("knots")
cross["v_wind"] = cross["v_wind"].metpy.convert_units("knots")
cross["t_wind"], cross["n_wind"] = mpcalc.cross_section_components(
    cross["u_wind"], cross["v_wind"]
)


# %% [markdown]
# Create figure

# %%
fig = plt.figure(1, figsize=(18, 9))
ax = plt.axes()

rh_contour = ax.contourf(
    cross["index"],
    cross["isobaric"],
    cross["Relative_humidity"],
    levels=np.arange(0, 1.05, 0.05),
    cmap="YlGnBu",
)

rh_colorbar = fig.colorbar(rh_contour)

theta_contour = ax.contour(
    cross["index"],
    cross["isobaric"],
    cross["Potential_temperature"],
    levels=np.arange(250, 450, 5),
    colors="k",
    linewidths=2,
)

theta_contour.clabel(
    theta_contour.levels[1::2],
    fontsize=8,
    colors="k",
    inline=1,
    inline_spacing=8,
    fmt="%i",
    rightside_up=True,
    use_clabeltext=True,
)

wind_slc_vert = list(range(0, 19, 2)) + list(range(19, 29))
wind_slc_horz = slice(5, 100, 5)

ax.barbs(
    cross["index"][wind_slc_horz],
    cross["isobaric"][wind_slc_vert],
    cross["t_wind"][wind_slc_vert, wind_slc_horz],
    cross["n_wind"][wind_slc_vert, wind_slc_horz],
    color="k",
)

ax.fill_between(
    cross["index"],
    cross["topo_pressure"],
    cross["isobaric"][0],
    edgecolor="black",
    facecolor="gray",
    zorder=2,
)

# Create x-axis ticks for lat, lon pairs
xticks = np.arange(10, 100, 15)
ax.set_xticks(np.concatenate([[0], xticks, [99]]))

# Adjust y-axis to log-scale and define pressure level ticks
ax.set_yscale("symlog")
ax.set_ylim(cross["isobaric"].max(), cross["isobaric"].min())
ax.set_yticks(np.arange(1000, 50, -100))

# Get Cartopy CRS object via MetPy xarray accessor
# and create inset map
data_crs = data["Geopotential_height"].metpy.cartopy_crs
ax_inset = fig.add_axes([0.125, 0.654, 0.25, 0.25], projection=data_crs)

ax_inset.contour(
    data["x"],
    data["y"],
    data["Geopotential_height"].sel(isobaric=500.0),
    levels=np.arange(5100, 6000, 60),
    cmap="inferno",
)

# Mark ends of cross section path and draw a line between
endpoints = data_crs.transform_points(
    ccrs.Geodetic(), *np.vstack([start, end]).transpose()[::-1]
)
ax_inset.scatter(endpoints[:, 0], endpoints[:, 1], c="k", zorder=2)
ax_inset.plot(cross["x"], cross["y"], c="k", zorder=2)

# Add geographic features
ax_inset.coastlines()
ax_inset.add_feature(cfeature.STATES.with_scale("50m"), edgecolor="k", alpha=0.2, zorder=0)

#
ax_inset.text(
    endpoints[0, 0] - 400000,
    endpoints[0, 1] - 350000,
    "A",
    transform=data_crs,
    fontweight="bold",
    color="white",
    path_effects=[withStroke(linewidth=3, foreground="black")],
)
ax_inset.text(
    endpoints[1, 0] + 200000,
    endpoints[1, 1] - 250000,
    "B",
    transform=data_crs,
    fontweight="bold",
    color="white",
    path_effects=[withStroke(linewidth=3, foreground="black")],
)

# Set axis and tick labels

ticklabels = [
    f"{lat:.4}, {lon:.4}"
    for (lat, lon) in zip(
        cross["lat"].sel(index=xticks).values, cross["lon"].sel(index=xticks).values
    )
]

ax.set_xticklabels(np.concatenate([["A"], ticklabels, ["B"]]))
ax.set_yticklabels(np.arange(1000, 50, -100))
ax.set_ylabel(f"Pressure (hPa)")
ax.set_xlabel("Latitude (degrees north), Longitude (degrees east)")
rh_colorbar.set_label("Relative Humidity")

fig.savefig("../output/fig3_cross_section.png", dpi=600, bbox_inches="tight")

# %% [markdown]
# ### Draft caption
# Vertical cross section of relative humidity (shaded, dimensionless), potential temperature (contours, K), and wind (barbs, knots) components tangential and normal to the plane of the cross section. Latitude, longitude coordinates along the cross section path are provided along the x-axis, vertical pressure levels are provided along the y-axis. Inset (top-left corner) is a map of the trace of the cross-section and contours of 500 hPa geopotential height. Data from North American Regional Reanalysis (NARR) valid April 04 1987 1800UTC.
