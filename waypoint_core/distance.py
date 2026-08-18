"""Distance value type for the Waypoint engine."""

KM_PER_MILE = 1.609344


class Distance:
    """A distance with a magnitude and a unit.

    Purpose:
        Represent a distance in kilometers or miles and allow safe
        conversion between the two. Rejects negative magnitudes.
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
        """Return a new Distance converted to the other unit.

        Purpose:
            Convert this distance to km or mi.
        Arguments:
            to_unit (str): the target unit, "km" or "mi".
        Returns:
            A new Distance in the target unit.
        """
        if to_unit not in self.ALLOWED_UNITS:
            raise ValueError("unit must be 'km' or 'mi'")

        if to_unit == self._unit:
            return Distance(self._magnitude, self._unit)

        if self._unit == "km" and to_unit == "mi":
            return Distance(self._magnitude / KM_PER_MILE, "mi")

        return Distance(self._magnitude * KM_PER_MILE, "km")
