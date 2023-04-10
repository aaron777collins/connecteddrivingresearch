import math
from geographiclib.geodesic import Geodesic
from geopy import distance


class MathHelper:
    @staticmethod
    # direction_angle is north at 0 (- is to the west, + is to the east)
    def direction_and_dist_to_lat_long_offset(orig_lat, orig_long, direction_angle, distance_meters):
        geod = Geodesic.WGS84

        theta = 0 #direction from North, clockwise
        newAngle = theta + direction_angle #(direction angle degrees to the right of North)

        g = geod.Direct(orig_lat, orig_long, newAngle, distance_meters)

        lat2 = g['lat2']
        lon2 = g['lon2']
        return (lat2, lon2)

    @staticmethod
    def dist_between_two_points(lat1, lon1, lat2, lon2):
        geod = Geodesic.WGS84
        lat1_rad = MathHelper.deg2rad(lat1)
        lon1_rad = MathHelper.deg2rad(lon1)
        lat2_rad = MathHelper.deg2rad(lat2)
        lon2_rad = MathHelper.deg2rad(lon2)
        distance = geod.Inverse(lat1_rad, lon1_rad, lat2_rad, lon2_rad)
        return distance['s12']

    @staticmethod
    def deg2rad(deg):
        return deg * (math.pi/180)
