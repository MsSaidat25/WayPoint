from waypoint_core.distance import Distance
from waypoint_core.trail import (
    Trail, DayHike, BackpackingRoute, TrailRun, GuidedDayHike, RatedDayHike
)

print("=== WP-202 Distance operators ===")
print("add:", Distance(3, "km") + Distance(2, "km"))
print("sub equals 3km:", (Distance(5, "km") - Distance(2, "km")) == Distance(3, "km"))
print("sorted:", sorted([Distance(5, "km"), Distance(1, "km"), Distance(3, "km")]))
print("mi > km:", Distance(1, "mi") > Distance(1, "km"))
print("repr:", repr(Distance(4, "mi")))

print()
print("=== WP-201 cannot instantiate abstract Trail ===")
try:
    Trail("t0", "Base", Distance(1, "km"), 10, "easy")
except TypeError as e:
    print("Trail() raised TypeError as expected")

print()
print("=== WP-206 polymorphic loop over mixed types ===")


class FakeTrail:
    """Duck-typed trail that inherits nothing. (WP-206)"""

    def __init__(self, name):
        self.name = name

    def estimated_time(self):
        return 1.0

    def summary(self):
        return "Fake: " + self.name


trails = [
    DayHike("d1", "River Loop", Distance(8, "km"), 200, "moderate"),
    BackpackingRoute("b1", "Long Ridge", Distance(30, "km"), 1500, "hard", days=3),
    TrailRun("r1", "Sprint Path", Distance(6, "km"), 100, "easy"),
    GuidedDayHike("g1", "Guided Loop", Distance(8, "km"), 200, "easy", guide_name="Sam"),
    FakeTrail("Mystery"),
]

for t in trails:
    print(t.summary(), "->", round(t.estimated_time(), 2), "hrs")

print()
print("=== WP-205 mixins + MRO ===")
rated = RatedDayHike("rd1", "Scenic Loop", Distance(10, "km"), 500, "moderate")
rated.add_rating(5)
rated.add_rating(3)
print("grade %:", round(rated.grade_percent(), 2))
print("avg rating:", rated.average_rating())
print("MRO:", [c.__name__ for c in RatedDayHike.__mro__])
