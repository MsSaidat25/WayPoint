from django.db import models


class Park(models.Model):
    # a park groups many trails (WP-701)
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Trail(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("moderate", "Moderate"),
        ("hard", "Hard"),
        ("expert", "Expert"),
    ]

    name = models.CharField(max_length=200)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2)
    elevation_gain = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    is_open = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)
    # link each trail to a park (WP-702)
    # on_delete=SET_NULL: if a park is deleted, keep its trails but leave
    # them unassigned rather than deleting hiking data. null=True lets
    # existing rows and unassigned trails hold no park.
    park = models.ForeignKey(
        Park,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trails",
    )

    def __str__(self):
        return self.name
