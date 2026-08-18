"""Trail hierarchy for the Waypoint engine."""

from abc import ABC, abstractmethod
from waypoint_core.distance import Distance


class Trail(ABC):
    """Abstract base trail. (WP-201)

    Purpose:
        Define the shared shape of every trail and force each concrete
        type to provide its own estimated_time() and summary().
    Arguments:
        trail_id (str): unique id.
        name (str): trail name.
        distance (Distance): trail length.
        elevation_gain_m (float): elevation gain in meters.
        difficulty (str): must be in ALLOWED_DIFFICULTIES.
    Returns:
        A Trail subclass instance (Trail itself cannot be instantiated).
    """

    ALLOWED_DIFFICULTIES = ("easy", "moderate", "hard")
    default_unit = "km"

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty):
        self.trail_id = trail_id
        self.name = name
        self.distance = distance
        self.elevation_gain_m = elevation_gain_m
        self._difficulty = None
        self.set_difficulty(difficulty)

    @property
    def difficulty(self):
        return self._difficulty

    def set_difficulty(self, value):
        if value not in self.ALLOWED_DIFFICULTIES:
            raise ValueError("difficulty must be easy, moderate, or hard")
        self._difficulty = value

    @staticmethod
    def is_valid_difficulty(value):
        return value in Trail.ALLOWED_DIFFICULTIES

    @staticmethod
    def is_valid_elevation(value):
        return value >= 0

    @classmethod
    def from_dict(cls, data):
        unit = data.get("unit", cls.default_unit)
        distance = Distance(data["distance"], unit)
        return cls(data["id"], data["name"], distance, data["elevation_gain_m"], data["difficulty"])

    def __eq__(self, other):
        if not isinstance(other, Trail):
            return NotImplemented
        return self.trail_id == other.trail_id

    def __hash__(self):
        return hash(self.trail_id)

    @abstractmethod
    def estimated_time(self):
        """Return estimated time in hours. Each type computes its own."""
        pass

    @abstractmethod
    def summary(self):
        """Return a short readable summary of the trail."""
        pass


class DayHike(Trail):
    """A single-day hike. (WP-201)

    Pacing: about 4 km per hour walking speed.
    """

    PACE_KM_PER_HOUR = 4.0

    def estimated_time(self):
        return self.distance.convert("km").magnitude / self.PACE_KM_PER_HOUR

    def summary(self):
        return "Day hike: " + self.name + " (" + self.difficulty + ")"


class BackpackingRoute(Trail):
    """A multi-day route. (WP-201, WP-203, WP-204)

    Pacing is slower with a heavy pack, and it spans multiple days.
    """

    PACE_KM_PER_HOUR = 2.5

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty, days):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        self.days = days

    def estimated_time(self):
        return self.distance.convert("km").magnitude / self.PACE_KM_PER_HOUR

    def summary(self):
        return "Backpacking: " + self.name + " over " + str(self.days) + " days"

    def packing_list(self):
        """Override point: multi-day trips need more gear. (WP-204)"""
        return ["tent", "stove", "sleeping bag", "map"]


class TrailRun(Trail):
    """A trail run. (WP-201)

    Pacing: much faster running speed.
    """

    PACE_KM_PER_HOUR = 8.0

    def estimated_time(self):
        return self.distance.convert("km").magnitude / self.PACE_KM_PER_HOUR

    def summary(self):
        return "Trail run: " + self.name


class GuidedDayHike(DayHike):
    """A guided day hike, one level deeper than DayHike. (WP-203, WP-204)

    Adds a guide_name field and runs a bit slower because the group
    stops for the guide's explanations.
    """

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty, guide_name):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        self.guide_name = guide_name

    def estimated_time(self):
        # extend rather than replace: take the base time and add 20% (WP-204)
        base = super().estimated_time()
        return base * 1.2

    def summary(self):
        return "Guided day hike: " + self.name + " with " + self.guide_name


class ElevationMixin:
    """Mixin that computes grade percent. (WP-205)"""

    def grade_percent(self):
        km = self.distance.convert("km").magnitude
        meters = km * 1000
        if meters == 0:
            return 0
        return (self.elevation_gain_m / meters) * 100


class RatingMixin:
    """Mixin that tracks star ratings and averages them. (WP-205)"""

    def add_rating(self, stars):
        if not hasattr(self, "_ratings"):
            self._ratings = []
        self._ratings.append(stars)

    def average_rating(self):
        ratings = getattr(self, "_ratings", [])
        if not ratings:
            return 0
        return sum(ratings) / len(ratings)


class RatedDayHike(ElevationMixin, RatingMixin, DayHike):
    """A DayHike composed with both mixins. (WP-205)

    MRO (method resolution order):
        RatedDayHike -> ElevationMixin -> RatingMixin -> DayHike -> Trail -> ABC -> object
    Python checks each class left to right, so mixin methods are found
    before the DayHike/Trail methods, and DayHike's own methods still win
    over anything further down.
    """
    pass
