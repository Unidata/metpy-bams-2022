import geopandas

from metpy.cbook import get_test_data
from metpy.plots import MapPanel, PanelContainer, PlotGeometry


day1_outlook = geopandas.read_file(
    get_test_data("spc_day1otlk_20210317_1200_lyr.geojson")
)


geo = PlotGeometry()
geo.geometry = day1_outlook["geometry"]
geo.fill = day1_outlook["fill"]
geo.stroke = day1_outlook["stroke"]
geo.labels = day1_outlook["LABEL"]
geo.label_fontsize = "large"

panel = MapPanel()
panel.title = " "
panel.title_fontsize = 18
panel.plots = [geo]
panel.area = [-120, -75, 25, 50]
panel.projection = "lcc"
panel.layers = ["lakes", "land", "ocean", "states", "coastline", "borders"]

pc = PanelContainer()
pc.size = (18, 9)
pc.panels = [panel]
pc.save("images/plotgeom.png", dpi=600, bbox_inches="tight")

# draft caption
# NOAA/NWS Storm Prediction Center (SPC) March 17 2021 1200 UTC Day 1 Convective Outlook recreated using metpy.plots.PlotGeometry. PlotGeometry is provided as part of MetPy's declarative plotting interface. Data from SPC GeoJSON archive.
