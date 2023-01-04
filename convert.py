import json
from pykml import parser

# Read the KML file into a bytes object
with open('input.kml', 'rb') as f:
  kml_bytes = f.read()

# Parse the KML bytes
root = parser.fromstring(kml_bytes)

# Create an empty list
location_list = []

def process_element(element):
  """Recursively process an element and its children."""
  if element.tag.endswith('}Placemark'):
    hasValidTag = False

    try:
      hasValidTag = hasattr(element.Point, "coordinates")
    except:
      hasValidTag = False

    if hasValidTag:
      lat = float(element.Point.coordinates.text.split(',')[0])
      lon = float(element.Point.coordinates.text.split(',')[1])
      print(lat, lon, type(lat), type(lon))
      location = {
        'name': element.name.text,
        'description': element.description.text if hasattr(element, 'description') else None,
        'latitude': lat,
        'longitude': lon,
      }
      print(location)
      location_list.append(location)
  elif element.tag.endswith('}Folder'):
     # Skip folders with specific names
    if element.name.text not in ['Tracks', 'Waypoints', 'Points']:
      # Process the element's children
      for child in element.iterchildren():
        process_element(child)
  else:
    # Process the element's children
    for child in element.iterchildren():
      process_element(child)

# Process the root element
process_element(root)

# Create the JSON object
json_data = {
  'location': location_list
}

# Write the JSON object to a file
with open('output.json', 'w') as f:
  json.dump(json_data, f)
