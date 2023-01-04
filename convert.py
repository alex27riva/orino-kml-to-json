#!/usr/bin/env python3
import json
import re
import argparse
from pykml import parser as kparser

# Parse arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('--desc',
                    action='store_true',
                    default=False,
                    help='Skip elements with empty descriptions')
parser.add_argument('--input_file',
                    type=str,
                    default='input.kml',
                    help='The KML file to convert')
args = parser.parse_args()

# Read the KML file into a bytes object
with open(args.input_file, 'rb') as f:
  kml_bytes = f.read()

# Parse the KML bytes
root = kparser.fromstring(kml_bytes)

# Create an empty list
location_list = []


def remove_tags(text):
  """Remove HTML tags from a string"""
  clean = re.compile('<.*?>')
  text = re.sub(clean, '', text)
  text = text.replace("\n", "")
  return text


def process_element(element):
  """Recursively process an element and its children."""
  if element.tag.endswith('}Placemark'):
    hasValidTag = False

    try:
      hasValidTag = hasattr(element.Point, "coordinates")
    except:
      hasValidTag = False

    if hasValidTag:
      # 0: longitude, 1: latitude
      lon = float(element.Point.coordinates.text.split(',')[0])
      lat = float(element.Point.coordinates.text.split(',')[1])
      name = element.name.text
      description = remove_tags(
          element.description.text).capitalize() if hasattr(
              element, 'description') else ""
      location = {
          'name': name.lower().capitalize(),
          'description': description,
          'latitude': lat,
          'longitude': lon,
      }
      print(location)
      if args.desc:
        if description:
          location_list.append(location)
      else:
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
json_data = {'location': location_list}

# Write the JSON object to a file
with open('output.json', 'w', encoding="utf-8") as f:
  json.dump(json_data, f, ensure_ascii=False)
