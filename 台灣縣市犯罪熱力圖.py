import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# 1. Load the CSV file
file_path = "主要警政統計指標2.csv"
df = pd.read_csv(file_path)

# Show the first few rows
print(df.head())

# 2. Load Taiwan shapefile or GeoJSON (example from online)
# Taiwan county boundaries from public GeoJSON
geo_url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/taiwan.geojson"
gdf = gpd.read_file(geo_url)

# 3. Inspect the county names
print("GeoJSON counties:", gdf["name"].unique())

# 4. Preprocess: Rename columns for merging
df.rename(columns={df.columns[0]: "County"}, inplace=True)  # Assuming first column is county name
gdf.rename(columns={"name": "County"}, inplace=True)

# Merge GeoDataFrame with CSV
merged = gdf.merge(df, on="County", how="left")

# 5. Plot the data (adjust column name based on your CSV)
plt.figure(figsize=(10, 12))
merged.plot(column=merged.columns[2], cmap='OrRd', legend=True, edgecolor='black')
plt.title("Taiwan Map with Police Statistics", fontsize=15)
plt.axis('off')
plt.show()