from django.db import models

from base.models import BaseUUIModel

# Create your models here.


class Profile(BaseUUIModel):
    user = models.UUIDField()
    business_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.business_name
