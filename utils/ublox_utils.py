
import csv
# from fastkml import kml
# from shapely.geometry import Point, Polygon
# from shapely.geometry import shape
# import pyproj

def decode_tow(tim_tm):
    # Extract the rising edge Time of Week (TOW)
    towR = int.from_bytes(tim_tm[6 + 8:6 + 12], byteorder='little', signed=False)
    return towR/1000

def in_box():
    return True

def extract_polygons_from_kml(kml_file_path):
    # with open(kml_file_path, 'r') as file:
    #  kml_content = file.read()

    # k = kml.KML()
    # k.from_string(kml_content)
    k = kml.KML.parse(kml_file_path)

    # Collect polygons from the KML file
    polygons = []
    for feature in k.features:
        for placemark in feature.features:
            geometry = placemark.geometry
            if geometry and geometry.geom_type == 'Polygon':
                polygons.append(shape(geometry))
    
    return polygons

# Function to check if a GPS location is in the polygons
def is_location_in_kml_area(lat, lon, kml_file_path):
    point = Point(lon, lat)  # Note: Shapely uses (lon, lat) order
    polygons = extract_polygons_from_kml(kml_file_path)
    
    for polygon in polygons:
        if point.within(polygon):
            return True
    return False

# # Example usage
# kml_file_path = './map.geo.admin.ch_KML_20241211151658.kml'
# latitude = 46.681438
# longitude = 7.892339

# if is_location_in_kml_area(latitude, longitude, kml_file_path):
#     print("The location is within the KML area.")
# else:
#     print("The location is NOT within the KML area.")


def log_gps_event(data, filename):
    tow = decode_tow(data)
    with open(filename, 'a', newline='') as log_file:
        writer = csv.writer(log_file)
        writer.writerow([tow])
