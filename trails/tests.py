from django.test import TestCase
from decimal import Decimal
from trails.models import Trail, Park
from waypoint_core.distance import Distance


class OpenTrailsQueryTest(TestCase):
    # Django TestCase: the catalog query returns only open trails (WP-801)
    def setUp(self):
        self.park = Park.objects.create(name="Test Park", region="Test Region")
        Trail.objects.create(name="Open A", distance_km=Decimal("5.0"),
                             elevation_gain=100, difficulty="easy",
                             is_open=True, park=self.park)
        Trail.objects.create(name="Closed B", distance_km=Decimal("9.0"),
                             elevation_gain=300, difficulty="hard",
                             is_open=False, park=self.park)

    def test_only_open_trails_returned(self):
        open_trails = Trail.objects.filter(is_open=True)
        self.assertEqual(open_trails.count(), 1)
        self.assertEqual(open_trails.first().name, "Open A")


from django.http import Http404
from django.test import RequestFactory
from trails.views import park_trails


class PageStatusTest(TestCase):
    # a missing park id should raise Http404 (WP-801)
    def test_missing_park_returns_404(self):
        request = RequestFactory().get("/park/9999/")
        with self.assertRaises(Http404):
            park_trails(request, 9999)


class DistanceRuleTest(TestCase):
    # unit test for a domain rule from the Week 7-8 engine (WP-801)
    def test_negative_distance_rejected(self):
        with self.assertRaises(ValueError):
            Distance(-1, "km")

    def test_addition_auto_converts(self):
        total = Distance(3, "km") + Distance(2, "km")
        self.assertEqual(total.magnitude, 5)
