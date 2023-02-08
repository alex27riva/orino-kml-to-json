# orino-kml-to-json

Python script to convert .kml file to .json for the OrinoSmartVillage project.

## Installation

- `pip3 install -r requirements.txt`

## Usage

Make Python file executable:

- `chmod +x convert.py`

### Example

`./convert.py --input orino_experience.kml --out places.json --desc`

### Help

```text
usage: convert.py [-h] [--input INPUT] [--output OUTPUT] [--desc]

options:
  -h, --help       show this help message and exit
  --input INPUT    The KML file to convert
  --output OUTPUT  The converted json file
  --desc           Skip elements with empty descriptions
```
