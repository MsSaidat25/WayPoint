"""Distance value type for the Waypoint engine.

Design note on mixed units:
When two distances use different units, arithmetic and comparisons
auto-convert both to kilometers before operating, and the result is
returned in kilometers. We auto-convert rather than reject because a
distance should behave like a real quantity, so 3 km + 2 mi should just
work. Kilometers is chosen as the common unit because it is the
platform default.
"""

KM_PER_MILE = 1.609344


class Distance:
    """A distance with a magnitude and a unit.

    Purpose:
        Represent a distance in km or mi, allow conversion, and support
        arithmetic and comparison like a real quantity.
    Arguments:
        magnitude (float): the numeric length, must not be negative.
        unit (str): either "km" or "mi".
    Returns:
        A Distance object.
    """

    ALLOWED_UNITS = ("km", "mi")

    def __init__(self, magnitude, unit):
        if magnitude < 0:
            raise ValueError("magnitude cannot be negative")
        if unit not in self.ALLOWED_UNITS:
            raise ValueError("unit must be 'km' or 'mi'")
        self._magnitude = magnitude
        self._unit = unit

    @property
    def magnitude(self):
        """Read-only access to the magnitude."""
        return self._magnitude

    @property
    def unit(self):
        """Read-only access to the unit."""
        return self._unit

    def convert(self, to_unit):
        """Return a new Distance converted to the given unit."""
        if to_unit not in self.ALLOWED_UNITS:
            raise ValueError("unit must be 'km' or 'mi'")
        if to_unit == self._unit:
            return Distance(self._magnitude, self._unit)
        if self._unit == "km" and to_unit == "mi":
            return Distance(self._magnitude / KM_PER_MILE, "mi")
        return Distance(self._magnitude * KM_PER_MILE, "km")

    def _km_value(self):
        """Return this distance's magnitude in kilometers."""
        if self._unit == "km":
            return self._magnitude
        return self._magnitude * KM_PER_MILE

    def __add__(self, other):
        """Add two distances, auto-converting to km."""
        return Distance(self._km_value() + other._km_value(), "km")

    def __sub__(self, other):
        """Subtract two distances in km; result must not be negative."""
        return Distance(self._km_value() - other._km_value(), "km")

    def __eq__(self, other):
        """Two distances are equal if their km values match closely."""
        if not isinstance(other, Distance):
            return NotImplemented
        return abs(self._km_value() - other._km_value()) < 0.0001

    def __lt__(self, other):
        """Compare distances by their km value."""
        return self._km_value() < other._km_value()

    def __gt__(self, other):
        """Compare distances by their km value."""
        return self._km_value() > other._km_value()

    def __hash__(self):
        """Hash by rounded km value so equal distances hash equally."""
        return hash(round(self._km_value(), 4))

    def __str__(self):
        """Readable text like '5 km'."""
        return str(self._magnitude) + " " + self._unit

    def __repr__(self):
        """Unambiguous form for developers."""
        return "Distance(" + repr(self._magnitude) + ", " + repr(self._unit) + ")"
