from django.db import models

from base.models import BaseUUIModel, Country, Location

# Create your models here.


class BusinessAddress(BaseUUIModel):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    zip_code = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "f{self.street_address}, {self.city}, {self.state}, {self.country}"


class Profile(BaseUUIModel):
    BUSINESS_CATEGORY = [
        (
            "local_experience",
            "Local experience (Restaurants, Beauty, Leisure & Services)",
        ),
        ("ticketed_events", "Ticketed Events"),
        ("hotels_travel", "Hotels & Travel"),
        ("goods_products", "Goods & Products"),
    ]
    user = models.UUIDField()
    business_name = models.CharField(max_length=255, null=True, blank=True)
    business_address = models.ForeignKey(BusinessAddress, on_delete=models.SET_DEFAULT, default=1)
    phone = models.CharField(max_length=20, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    business_category = models.CharField(
        default="local_experience", choices=BUSINESS_CATEGORY, max_length=100
    )

    def __str__(self):
        return self.business_name
