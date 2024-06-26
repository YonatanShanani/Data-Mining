import json
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from shapely.geometry import Point

# Load the JSON data
with open('./output/villains_data.json', 'r') as f:
    data = json.load(f)

# Extract place of birth information
places_of_birth = []
villains = data['female_villains'] + data['male_villains']

for villain in villains:
    place_of_birth = villain.get('place_of_birth', '')
    if place_of_birth:
        places_of_birth.append({
            'name': villain['name'],
            'place_of_birth': place_of_birth,
            'universe': villain['universe']
        })

# Geocode places of birth to get coordinates
geolocator = Nominatim(user_agent="villain_locator")

def geocode(place):
    try:
        location = geolocator.geocode(place)
        if location:
            return Point(location.longitude, location.latitude)
    except GeocoderTimedOut:
        return geocode(place)
    return None

geo_data = []
for place in places_of_birth:
    point = geocode(place['place_of_birth'])
    if point:
        geo_data.append({
            'name': place['name'],
            'universe': place['universe'],
            'geometry': point
        })

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(geo_data)

# Load the low resolution world map from a local path
world = gpd.read_file("./needed_files/ne_110m_admin_0_countries.shp")

# Drop "Antarctica" from the dataframe
world = world[world['CONTINENT'] != 'Antarctica']

# Initialize a final empty figure with higher DPI for higher resolution
fig = plt.figure(figsize=(20, 10), dpi=300)
ax = fig.add_subplot()

# Start by plotting a map of the world
world.boundary.plot(ax=ax, color="black", linewidth=0.5)

# Grab the unique set of continents, generate a unique color for each one, and initialize the list of patches
continents = world["CONTINENT"].unique()
colors = sns.color_palette("Set3", len(continents))
patches = []

# Loop over the continent names and corresponding colors
for (continent_name, color) in list(zip(continents, colors)):
    # Grab all countries that belong to the continent, then plot each of the continents, giving each a unique color
    continent = world[world["CONTINENT"] == continent_name]
    continent.plot(ax=ax, color=color, alpha=0.5)

    # Generate a patch for the current continent
    patch = mpatches.Patch(label=continent_name, color=color)
    patches.append(patch)

# Add the patches to the map
ax.legend(handles=patches, loc="lower left")

# Plot the villains on the map
gdf.plot(ax=ax, marker='o', color='red', markersize=50, alpha=0.6)

# Turn off axis ticks
ax.set_xticks([])
ax.set_yticks([])

# Set the plot title
plt.title("Villains' Places of Birth with GeoPandas")
plt.show()
