from django.contrib.gis.db import models

# Create your models herie.

class Route(models.Model):
    start = models.CharField(max_length = 30)
    end = models.CharField(max_length = 30)
    coordinates = models.LineStringField()
    objects = models.GeoManager()

