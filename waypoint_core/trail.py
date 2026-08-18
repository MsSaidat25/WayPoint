"""Trail class for the Waypoint engine."""

from waypoint_core.distance import Distance


class Trail:
    """A hiking trail with a guarded difficulty.

    Purpose:
        Describe a single trail and protect its state, so the difficulty
        can only ever be set to an allowed value.
    Arguments:
        trail_id (str): unique id for the trail.
        name (str): the trail name.
        distance (Distance): the trail length.
        elevation_gain_m (float): total elevation gain in meters.
        difficulty (str): starting difficulty, must be in ALLOWED_DIFFICULTIES.
    Returns:
        A Trail object.
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
        """Read-only access to the difficulty."""
        return self._difficulty

    def set_difficulty(self, value):
        """Set the difficulty after checking it is allowed.

        Purpose:
            Guard the difficulty so it can only be a valid value.
        Arguments:
            value (str): the new difficulty.
        Returns:
            None.
        """
        if value not in self.ALLOWED_DIFFICULTIES:
            raise ValueError("difficulty must be easy, moderate, or hard")
        self._difficulty = value

    @staticmethod
    def is_valid_difficulty(value):
        """Check a difficulty string is allowed.

        Purpose:
            Validate a difficulty without needing a Trail instance.
        Arguments:
            value (str): the difficulty to check.
        Returns:
            True if valid, False otherwise.
        """
        return value in Trail.ALLOWED_DIFFICULTIES

    @staticmethod
    def is_valid_elevation(value):
        """Check an elevation value is not negative.

        Purpose:
            Validate elevation gain without needing a Trail instance.
        Arguments:
            value (float): the elevation gain in meters.
        Returns:
            True if valid, False otherwise.
        """
        return value >= 0

    @classmethod
    def from_dict(cls, data):
        """Build a Trail from an API-shaped dictionary.

        Purpose:
            Create a Trail from raw data, using the platform default unit
            when the data does not name one.
        Arguments:
            data (dict): keys id, name, distance, elevation_gain_m, difficulty,
                and an optional unit.
        Returns:
            A new Trail object.
        """
        unit = data.get("unit", cls.default_unit)
        distance = Distance(data["distance"], unit)
        return cls(
            data["id"],
            data["name"],
            distance,
            data["elevation_gain_m"],
            data["difficulty"],
        )

    def __eq__(self, other):
        """Compare two trails by their id.

        Purpose:
            Let imports de-duplicate trails that share an id even when
            their other data differs.
        Arguments:
            other (Trail): the trail to compare against.
        Returns:
            True if both are Trails with the same id, False otherwise.
        """
        if not isinstance(other, Trail):
            return NotImplemented
        return self.trail_id == other.trail_id

    def __hash__(self):
        """Hash by id so equal trails hash equally."""
        return hash(self.trail_id)
