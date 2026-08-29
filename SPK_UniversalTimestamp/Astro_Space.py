"""
Astro_Space — spatial primitives for observer locations on Earth.

**Purpose.**  Wrap the pieces of `pyproj` and `shapely.geometry`
that the astronomical-calendar code needs into a single small
class (`psoEarth`, "point on the surface of Earth") with
value-semantic equality, hashability, and a WGS84 geodesic
distance/azimuth calculator.

**Public surface (star-exported via `__init__.py`).**
    `psoEarth` (class) — constructor takes `(latitude, longitude,
    elevation=0.0)` in degrees / metres; exposes `psoAzimuth_to`
    which returns `(forward_azimuth, backward_azimuth, distance)`
    as `Decimal` triples quantised to 7 decimal degrees / 0.1 m.

**Known issue.**  `psoEarth.__ne__` passes `other.point` (a shapely
`Point`) into `self.__eq__` (which expects `psoEarth`), so it
returns `True` for values that `__eq__` reports as equal.  Tracked
as backlog entry B-02 in `docs/TODO_BACKLOG.md`; the line carries
an inline ``# type: ignore[attr-defined]`` and ``BUG (B-02)`` marker.
Fixing the behavior is a future plan's job — PL-01 Phase 4 is
non-behavioral.

**Module-level state.**  `_geod_earth = pyproj.Geod(ellps="WGS84")`
is constructed once at import; `pyproj.Geod` is thread-safe for
`inv` calls so sharing across threads is fine.

**Not in scope.**  Planetary bodies other than Earth; time/space
coupling (see `CC14_Time_and_Astronomy` for observer-time coupling).

**Change history.**  See `CHANGELOG.md`.
"""

from decimal import Decimal

import pyproj
from shapely.geometry import Point

_geod_earth = pyproj.Geod(ellps="WGS84")

class psoEarth:
    """
    Point on the surface of Earth — an observer location with WGS84
    geodesic operations.

    Instances are hashable and compare by the wrapped `shapely.Point`
    coordinates.  Elevation is captured but not currently used by
    `psoAzimuth_to` (the pyproj geodesic is 2-D on the ellipsoid).

    Attributes:
        point:  `shapely.geometry.Point` holding `(longitude,
            latitude, elevation)` in that order (shapely's XYZ
            convention, NOT the geographic lat/lon convention that
            the constructor accepts).
    """
    point : Point
    def __init__(self, latitude: float, longitude: float, elevation: float = 0.0) -> None:
        """
        Construct a `psoEarth` at the given geographic position.

        Args:
            latitude:   Degrees North (−90 .. +90).  Not range-checked.
            longitude:  Degrees East (−180 .. +180).  Not range-checked.
            elevation:  Metres above the WGS84 ellipsoid.  Defaults
                to zero (mean sea level).

        Notes:
            Stores as `Point(longitude, latitude, elevation)` —
            shapely wants (x, y, z), and geographic x=longitude.
        """
        self.point = Point(longitude, latitude, elevation)
        return
    def __str__(self) -> str:
        """Return `str(self.point)` (shapely's WKT-ish form)."""
        return str(self.point)
    def __repr__(self) -> str:
        """Return `repr(self.point)` (shapely's `Point(x y z)` form)."""
        return repr(self.point)
    def __eq__(self, other: object) -> bool:
        """
        Value-equality: `True` iff `other` is a `psoEarth` with an
        equal underlying `Point`.
        """
        if isinstance(other, psoEarth):
            return self.point.__eq__(other.point)
        return False
    def __ne__(self, other: object) -> bool:
        """
        Inequality — buggy per backlog B-02; do not use as a truth
        source until fixed.  See module docstring.
        """
        if isinstance(other, psoEarth):
            # BUG (B-02): passes other.point (Point) into self.__eq__ (expects psoEarth),
            # so __ne__ returns True for equal psoEarths.  Preserved for now per PL-01
            # Phase 4 "no behavioral changes"; fix belongs in a future plan.
            return not self.__eq__(other.point)  # type: ignore[attr-defined]
        return True
    def __hash__(self) -> int:
        """Hash by the wrapped `shapely.Point` — consistent with `__eq__`."""
        return hash(self.point)
    
        
    def psoAzimuth_to(self, to_pso: "psoEarth") -> tuple[Decimal, Decimal, Decimal]:
        """
        WGS84 geodesic from `self` to `to_pso`: forward azimuth,
        backward azimuth, and distance.

        Args:
            to_pso:  Destination `psoEarth`.

        Returns:
            `(forward, backward, distance)` as `Decimal` triple.
            Azimuths are in degrees clockwise from geographic North,
            quantised to 7 decimals (≈ 1.1 cm at the equator).
            Distance is in metres, quantised to 0.1 m.

        Raises:
            `TypeError`:  `to_pso` is not a `psoEarth` instance.
        """
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