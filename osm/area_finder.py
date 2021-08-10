# REFERENCE: https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python

import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class AreaFinder:
    area_list = []
    
    def __init__(self):
        # get area data
        areas = pd.read_json("local-area-boundary.json")\

        # get name and coordinates (polygon) list
        name_list = []
        corr_list = []
        for _, row in areas.iterrows():
            name_list.append(row['fields']['name'])
            # for some reason the coordinates are reversed
            coordinates = row['fields']['geom']['coordinates'][0]
            coordinates = map(self.to_lat_lon, coordinates)
            corr_list.append(coordinates)

        self.area_list = []
        for i in range(len(corr_list)):
            # create polygons
            polygon = Polygon(corr_list[i])
            self.area_list.append({"name": name_list[i], "polygon": polygon})

    def to_lat_lon(self, coor) -> (float, float):
        return (coor[1], coor[0])

    def get_area_name(self, lat, lon) -> str:
        point = Point(lat,lon)
        for area in self.area_list:
            if area['polygon'].contains(point):
                return area['name']
        return None
