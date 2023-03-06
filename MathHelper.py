from geographiclib.geodesic import Geodesic

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

