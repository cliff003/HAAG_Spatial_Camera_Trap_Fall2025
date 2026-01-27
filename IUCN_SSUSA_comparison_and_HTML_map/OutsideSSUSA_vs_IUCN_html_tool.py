# -------------------------------------------------------
# SSUSA outside vs. IUCN (U.S.-only) interactive map
# - Legend
# - Per-species layers for polygons and points
# - Search, Fullscreen, MiniMap, Measure
# -------------------------------------------------------
import os
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import Fullscreen, MiniMap, MeasureControl, Search

#Paths (edit if needed)
NON_OVERLAP_CSV = r"C:\Users\Bio Surplus\Downloads\CS8903\outputs\non_overlap_sites.csv"
IUCN_FILE       = r"C:\Users\Bio Surplus\Downloads\CS8903\IUCN_Data\MAMMALS_TERRESTRIAL_ONLY.shp"
OUTPUT_HTML     = r"C:\Users\Bio Surplus\Downloads\CS8903\SSUSA_outside_US_layercontrol_with_legend.html"

#Column names
LAT_COL = "Latitude"
LON_COL = "Longitude"
SPECIES_COL_RAW = "species_raw"
SPECIES_COL_KEY = "species_iucn_key"
DIST_COL = "distance_m_to_iucn"
SITE_COL = "site_id"

#Load data
outside = pd.read_csv(NON_OVERLAP_CSV)
if LAT_COL not in outside.columns or LON_COL not in outside.columns:
    raise KeyError(f"Expected '{LAT_COL}' and '{LON_COL}' in {NON_OVERLAP_CSV}")

#Keep a species label column for display
species_label = SPECIES_COL_RAW if SPECIES_COL_RAW in outside.columns else SPECIES_COL_KEY
if species_label not in outside.columns:
    raise KeyError("Expected species column not found in non_overlap_sites.csv")

iucn = gpd.read_file(IUCN_FILE).to_crs("EPSG:4326")

#Clip IUCN polygons to the US
print("Clipping IUCN polygons to the U.S. …")
usa_url = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"
usa = gpd.read_file(usa_url)
usa = usa[usa["ADMIN"] == "United States of America"].to_crs(iucn.crs)
iucn = gpd.overlay(iucn, usa, how="intersection")

#Canonical species key on IUCN
def _canon(s):
    return (s.astype(str).str.strip().str.replace(r"\s+"," ", regex=True).str.lower())

sp_col = None
for c in ["sci_name", "BINOMIAL", "scientificName", "species"]:
    if c in iucn.columns:
        sp_col = c
        break
if sp_col is None:
    raise KeyError("Could not find a species column in the IUCN shapefile.")
iucn["species_key"] = _canon(iucn[sp_col])

#Map
center_lat = float(outside[LAT_COL].mean())
center_lon = float(outside[LON_COL].mean())
m = folium.Map(location=[center_lat, center_lon], zoom_start=5, tiles="CartoDB positron")

#Legend (bottom-left)
legend_html = """
<div style="
    position: fixed; 
    bottom: 20px; left: 20px; z-index: 9999; 
    background: white; padding: 10px 12px; 
    border: 1px solid #bbb; border-radius: 6px; 
    box-shadow: 0 1px 4px rgba(0,0,0,0.2);
    font-size: 13px;
">
  <div style="font-weight:600; margin-bottom:6px;">Legend</div>
  <div style="display:flex; align-items:center; margin-bottom:4px;">
    <span style="display:inline-block;width:12px;height:12px;border-radius:6px;background:#d7191c;margin-right:6px;"></span>
    <span>SSUSA detection outside IUCN polygon</span>
  </div>
  <div style="display:flex; align-items:center; margin-bottom:2px;">
    <span style="display:inline-block;width:14px;height:10px;background:#3186cc;opacity:0.25;border:1px solid #3186cc;margin-right:6px;"></span>
    <span>IUCN range (U.S. portion)</span>
  </div>
  <div style="display:flex; align-items:center; margin-top:6px;">
    <span style="display:inline-block;width:12px;height:12px;border-radius:6px;background:#ff7f00;margin-right:6px;"></span>
    <span>Selected species detections</span>
  </div>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

#All outside points as red dots
all_points_group = folium.FeatureGroup(name="All outside detections", show=True)
for _, r in outside.iterrows():
    lat = float(r[LAT_COL]); lon = float(r[LON_COL])
    sp = str(r[species_label])
    site = r.get(SITE_COL, "")
    dist_m = r.get(DIST_COL, None)
    tip = f"{sp}"
    if site: tip += f" | site: {site}"
    if pd.notna(dist_m):
        try:
            tip += f" | {float(dist_m):.0f} m to IUCN"
        except:
            pass
    folium.CircleMarker(
        location=[lat, lon],
        radius=3,
        color="#d7191c",
        fill=True,
        fill_opacity=0.9,
        tooltip=tip
    ).add_to(all_points_group)
all_points_group.add_to(m)

#Build per-species groups (polygons + points)
print("Adding species layers (polygons and points) …")
outside_gdf = gpd.GeoDataFrame(
    outside.copy(),
    geometry=gpd.points_from_xy(outside[LON_COL], outside[LAT_COL]),
    crs="EPSG:4326"
)
outside_gdf["species_key"] = _canon(outside_gdf[species_label])
iucn_groups = {sp: g for sp, g in iucn.groupby("species_key")}
species_present = sorted(outside_gdf["species_key"].dropna().unique())

for sp in species_present:
    if sp not in iucn_groups:
        continue

    poly_gdf = iucn_groups[sp].to_crs("EPSG:4326")
    pts_gdf = outside_gdf[outside_gdf["species_key"] == sp]

    #Polygon layer
    poly_group = folium.FeatureGroup(name=f"{sp} – IUCN range (U.S.)", show=False)
    folium.GeoJson(
        poly_gdf.__geo_interface__,
        style_function=lambda x: {"fillColor": "#3186cc", "color": "#3186cc",
                                  "weight": 1, "fillOpacity": 0.25},
        tooltip=f"{sp} (IUCN range)"
    ).add_to(poly_group)
    poly_group.add_to(m)

    #Species-specific points layer (orange)
    pts_group = folium.FeatureGroup(name=f"{sp} – detections", show=False)
    for _, r in pts_gdf.iterrows():
        tip = f"{sp}"
        site = r.get(SITE_COL, "")
        dist_m = r.get(DIST_COL, None)
        if site: tip += f" | site: {site}"
        if pd.notna(dist_m):
            try:
                tip += f" | {float(dist_m):.0f} m to IUCN"
            except:
                pass
        folium.CircleMarker(
            location=[r.geometry.y, r.geometry.x],
            radius=4,
            color="#ff7f00",
            fill=True,
            fill_opacity=0.9,
            tooltip=tip
        ).add_to(pts_group)
    pts_group.add_to(m)

#Useful plugins
Fullscreen(position="topleft").add_to(m)
MiniMap(toggle_display=True, position="bottomright").add_to(m)
MeasureControl(primary_length_unit='kilometers', secondary_length_unit='meters').add_to(m)

#Search plugin
pts_for_search = outside_gdf[[species_label, "geometry"]].copy()
pts_for_search.rename(columns={species_label: "species"}, inplace=True)
gj = folium.GeoJson(
    pts_for_search.to_json(),
    name="search_points",
    tooltip=folium.GeoJsonTooltip(fields=["species"], aliases=["Species"])
)
gj.add_to(m)
Search(
    layer=gj,
    search_label="species",
    placeholder="Search species…",
    collapsed=False
).add_to(m)

#Hide the default blue marker pin added by the search plugin
m.get_root().html.add_child(folium.Element("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    if (window.map && window.map.on) {
        window.map.on('search:locationfound', function(e) {
            if (e.layer && e.layer._icon) {
                e.layer._icon.style.display = 'none'; // hide pin
            }
            if (e.layer && e.layer._shadow) {
                e.layer._shadow.style.display = 'none'; // hide pin shadow
            }
        });
    }
});
</script>
"""))


#Layer control
folium.LayerControl(collapsed=False).add_to(m)

#Save
m.save(OUTPUT_HTML)
print(f"Saved map: {OUTPUT_HTML}")
