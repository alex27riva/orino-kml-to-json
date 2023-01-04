import json
from pykml import parser

# Read the KML file into a bytes object
with open('input.kml', 'rb') as f:
  kml_bytes = f.read()

# Parse the KML bytes
root = parser.fromstring(kml_bytes)

# Create an empty list
location_list = []

# Iterate over the placemarks in the KML data
for placemark in root.Document.Placemark:
  location = {
    'name': placemark.name.text,
    'description': placemark.description.text if hasattr(placemark, 'description') else None,
    'latitude': placemark.Point.coordinates.text.split(',')[0],
    'longitude': placemark.Point.coordinates.text.split(',')[1],
  }
  location_list.append(location)

# Create the JSON object
json_data = {
  'location': location_list
}

# Write the JSON object to a file
with open('output.json', 'w') as f:
  json.dump(json_data, f)
