#!/usr/bin/env python3
import sys
import json
import re
import argparse
import logging as log
from pykml import parser as kparser

# Logging
log.basicConfig(level=log.ERROR)

# Parse arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('--input',
                    type=str,
                    default='input.kml',
                    help='The KML file to convert')
parser.add_argument('--output',
                    type=str,
                    default='output.json',
                    help='The converted json file')
parser.add_argument('--desc',
                    action='store_true',
                    default=False,
                    help='Skip elements with empty descriptions')

args = parser.parse_args()

# Read the KML file into a bytes object
try:
  with open(args.input, 'rb') as f:
    kml_bytes = f.read()
except FileNotFoundError:
  log.error(f"The file '{args.input}' was not found.")
  sys.exit(1)

# Parse the KML bytes
root = kparser.fromstring(kml_bytes)

# Create an empty list
location_list = []


def remove_tags(text):
  """Remove HTML tags from a string"""
  clean = re.compile('<.*?>')
  text = re.sub(clean, '', text)
  text = text.replace("\n", "")
  text = text.strip()
  return text


def process_element(element):
  """Recursively process an element and its children."""
  if element.tag.endswith('}Placemark'):
    hasCoordinates = False

    try:
      hasCoordinates = hasattr(element.Point, "coordinates")
    except:
      hasCoordinates = False

    if hasCoordinates:
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
      log.debug(location)
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
try:
  with open(args.output, 'w', encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False)
except PermissionError:
  log.error(f"Failed writing {args.output} file, permission denied")
except Exception:
  log.error("Failed writing file")
