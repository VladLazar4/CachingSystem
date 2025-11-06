from django.db import models

class UserLocation(models.Model):
    nume = models.CharField(max_length=100)
    prenume = models.CharField(max_length=100)
    lat = models.FloatField()
    long = models.FloatField()
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)

    def __str__(self):
        return f"{self.nume} {self.prenume}"
