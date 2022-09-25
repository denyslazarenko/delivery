import os
from enum import Enum

import requests
import math
import flexpolyline as fp


class Direction(Enum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7

    def __str__(self):
        return self._value_


class HereAdapter:
    def __init__(self):
        # self.api_key = os.environ["HERE_API_KEY"]
        self.api_key = "1gcKNOSjKRVmBvaBAwE-VHzSJu5ti6DUJ4-DmGPJqVM"

    @staticmethod
    def calculate_bearing(coordinate1: tuple[float, float], coordinate2: tuple[float, float]):
        long1, lat1 = coordinate1
        long2, lat2 = coordinate2
        dist_lng = (long2 - long1)
        x = math.cos(math.radians(lat2)) * math.sin(math.radians(dist_lng))
        y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.cos(math.radians(dist_lng))
        bearing = math.atan2(x, y)
        bearing = math.degrees(bearing)
        return bearing

    @staticmethod
    def get_direction(coordinate1: tuple[float, float], coordinate2: tuple[float, float]):
        bearing = HereAdapter.calculate_bearing(coordinate1, coordinate2)
        bearing += 22.5
        bearing = bearing % 360
        bearing = int(bearing / 45)
        direction = Direction(bearing)
        return direction.name

    def get_navigation(self, origin: tuple[float, float], dest: tuple[float, float], transport_mode="bicycle") -> str:
        url = f"https://router.hereapi.com/v8/routes?transportMode={transport_mode}&origin={'%s,%s' % origin}&destination={'%s,%s' % dest}&"\
              f"return=polyline&apikey={self.api_key}"
        navigation_responce = requests.get(url)
        directions = ""
        if navigation_responce.status_code == 200:
            retrieved_navigation = navigation_responce.json()
            coordinates = fp.decode(retrieved_navigation['routes'][0]['sections'][0]['polyline'])
            cur_coordinate = coordinates[0]
            for next_coordinate in coordinates[1:]:
                directions += self.get_direction(cur_coordinate, next_coordinate)
                cur_coordinate = next_coordinate
        return directions

