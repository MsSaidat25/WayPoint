from waypoint_core.distance import Distance
from waypoint_core.trail import Trail
from waypoint_core.itinerary import Itinerary

# from_dict populates correctly
data = {"id": "t1", "name": "River Loop", "distance": 5, "elevation_gain_m": 200, "difficulty": "moderate"}
t1 = Trail.from_dict(data)
print("built:", t1.name, t1.distance.magnitude, t1.distance.unit, t1.difficulty)

# same id compare equal even with different data
t1_dup = Trail("t1", "Different Name", Distance(9, "km"), 999, "hard")
print("equal by id:", t1 == t1_dup)

# negative distance and bad difficulty raise
try:
    Distance(-1, "km")
except ValueError as e:
    print("neg distance raised:", e)

try:
    Trail.from_dict({"id": "x", "name": "X", "distance": 3, "elevation_gain_m": 10, "difficulty": "bad"})
except ValueError as e:
    print("bad difficulty raised:", e)

# convert round-trips
d = Distance(10, "km")
print("roundtrip:", round(d.convert("mi").convert("km").magnitude, 4))

# itinerary of three, and independence
t2 = Trail("t2", "Ridge", Distance(8, "km"), 350, "hard")
t3 = Trail("t3", "Creek", Distance(2, "km"), 50, "easy")
a = Itinerary("Trip A")
b = Itinerary("Trip B")
a.add_trail(t1)
a.add_trail(t2)
a.add_trail(t3)
print("total A:", a.total_distance().magnitude)
print("total B:", b.total_distance().magnitude)

# default unit change affects only new trails
Trail.default_unit = "mi"
t_new = Trail.from_dict({"id": "t4", "name": "New", "distance": 4, "elevation_gain_m": 10, "difficulty": "easy"})
print("new default unit:", t_new.distance.unit, "| old still:", t1.distance.unit)
Trail.default_unit = "km"
