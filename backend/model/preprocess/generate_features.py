import os

import torch
import h3
import pandas as pd
from h3 import LatLngPoly

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

processed_dir = os.path.join(BASE_DIR, '../datasets/processed')
os.makedirs(processed_dir, exist_ok=True)

all_hexes_path = os.path.join(processed_dir, 'all_hexes.pt')
crime_freq_path = os.path.join(processed_dir, 'crime_freq.csv')
graph_edges_path = os.path.join(processed_dir, 'graph_edges.pt')
cleaned_data_path = os.path.join(BASE_DIR, '../datasets/processed/cleaned_data.csv')

cleaned_data = pd.read_csv(cleaned_data_path, parse_dates=['date'])

coords_latitude = cleaned_data['latitude'].tolist()
coords_longitude = cleaned_data['longitude'].tolist()

max_lat, min_lat = max(coords_latitude), min(coords_latitude)
max_lon, min_lon = max(coords_longitude), min(coords_longitude)

polygon = LatLngPoly(
  [
    (min_lat, min_lon),
    (min_lat, max_lon),
    (max_lat, max_lon),
    (max_lat, min_lon),
    (min_lat, min_lon)
  ]
)

all_hexes = h3.polygon_to_cells(polygon, 9)

cleaned_data['h3_index'] = cleaned_data.apply(
    lambda row: h3.latlng_to_cell(row['latitude'], row['longitude'], 9),
    axis=1
)

earliest_date = cleaned_data['date'].min()
latest_date = cleaned_data['date'].max()

full_range = pd.date_range(start=earliest_date, end=latest_date, freq="D")

crime_freq = cleaned_data.groupby(['h3_index', 'date']).size().unstack(fill_value=0)
crime_freq = crime_freq.reindex(columns=full_range, fill_value=0)
crime_freq = crime_freq.reindex(all_hexes, fill_value=0)

hex_to_id = {}
for i, hex in enumerate(all_hexes):
    if hex not in hex_to_id:
        hex_to_id[hex] = i

graph_edges = []

for hex in all_hexes:
    neighbors = h3.grid_ring(hex, 1)
    for neighbor in neighbors:
        if neighbor in all_hexes:
            graph_edges.append([hex_to_id[hex], hex_to_id[neighbor]])

graph_edges = torch.tensor(graph_edges, dtype=torch.long).t().contiguous()

torch.save(all_hexes, all_hexes_path)
torch.save(graph_edges, graph_edges_path)
crime_freq.to_csv(crime_freq_path)

print("Saved all_hexes, crime_freq, and graph_edges.")