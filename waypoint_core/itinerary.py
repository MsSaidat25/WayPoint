"""Itinerary class for the Waypoint engine."""

from waypoint_core.distance import Distance


class Itinerary:
    """An ordered plan that HAS-A list of trails.

    Purpose:
        Group trails into a trip and report the total distance across them.
    Arguments:
        name (str): a label for the itinerary.
    Returns:
        An Itinerary object.
    """

    def __init__(self, name):
        self.name = name
        self._trails = []

    def add_trail(self, trail):
        """Add a trail to the end of the itinerary.

        Purpose:
            Append one trail to this itinerary's own list.
        Arguments:
            trail (Trail): the trail to add.
        Returns:
            None.
        """
        self._trails.append(trail)

    def total_distance(self, unit="km"):
        """Add up the distance of every trail in the itinerary.

        Purpose:
            Sum all trail distances, converting each to a common unit.
        Arguments:
            unit (str): the unit to report the total in.
        Returns:
            A Distance holding the total.
        """
        total = 0
        for trail in self._trails:
            converted = trail.distance.convert(unit)
            total += converted.magnitude
        return Distance(total, unit)
