from django.contrib.gis.db import models

# Create your models here

class Waypoint(models.Model):
    name = models.CharField(max_length = 30)
    geometry = models.PointField(srid = 4326)
    objects = models.GeoManager()

    def __unicode__(self):
        return "%s %s %s" % (self.name, self.geometry.x, self.geometry.y)
