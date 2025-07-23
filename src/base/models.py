import uuid

from django.db import models


# Create your models here.
class BaseUUIModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} {self.name}"


class Location(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    zip = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    city = models.CharField(max_length=100)
    state_id = models.CharField(max_length=100)
    state_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city} {self.state_id}"
