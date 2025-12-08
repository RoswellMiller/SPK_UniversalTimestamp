import pyproj
from shapely.geometry import Point
from decimal import Decimal

_geod_earth = pyproj.Geod(ellps="WGS84")

class psoEarth:
    point : Point
    def __init__(self, latitude: float, longitude: float, elevation: float = 0.0):
        """
        Initialize a point on the surface of Earth (s.o.e.) using latitude and longitude in degrees.     
        :param latitude: Latitude in degrees.
        :param longitude: Longitude in degrees.
        """
        self.point = Point(longitude, latitude, elevation)
        return
    def __str__(self):
        return str(self.point)
    def __repr__(self):
        return repr(self.point)
    def __eq__(self, other):
        if isinstance(other, psoEarth):
            return self.point.__eq__(other.point)
        return False
    def __ne__(self, other):
        if isinstance(other, psoEarth):
            return not self.__eq__(other.point)
        return True
    def __hash__(self):
        return hash(self.point)
    
        
    def psoAzimuth_to(self, to_pso) -> tuple[Decimal, Decimal, Decimal]:
        """Calculate geodesic distance to another point in meters"""
        if not isinstance(to_pso, psoEarth):
            raise TypeError("Can only calculate distance to another psoEarth object")
            
        lon1, lat1 = self.point.x, self.point.y
        lon2, lat2 = to_pso.point.x, to_pso.point.y
        f, b, d = _geod_earth.inv(lon1, lat1, lon2, lat2)
        f = Decimal(str(f)).quantize(Decimal('0.0000001'))  # forward azimuth in degrees
        b = Decimal(str(b)).quantize(Decimal('0.0000001'))  # backward azimuth in degrees
        d = Decimal(str(d)).quantize(Decimal('0.1'))
        return f, b, d  # forward, backward, distance in meters

    # def direction(self, to_pso) -> tuple[float , float]:
    #     """Calculate geodesic distance to another point in meters"""
    #     if not isinstance(to_pso, psoEarth):
    #         raise TypeError("Can only calculate distance to another psoEarth object")
            
    #     lon1, lat1 = self.point.x, self.point.y
    #     lon2, lat2 = to_pso.point.x, to_pso.point.y
        
    #     # Initialize geodesic calculator if needed
    #     #if not hasattr(self, '_geod'):
    #     #    self.add_geodesic_capabilities()
        
    #     forward, backward, _ = _geod_earth.inv(lon1, lat1, lon2, lat2)
    #     return forward, backward  # in degrees