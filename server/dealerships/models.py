from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Dealer(models.Model):
    name = models.CharField(max_length=160)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, db_index=True)
    address = models.CharField(max_length=240)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=30)
    website = models.URLField(blank=True)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ["state", "city", "name"]

    def __str__(self):
        return f"{self.name} ({self.city}, {self.state})"


class Review(models.Model):
    dealer = models.ForeignKey(Dealer, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="dealer_reviews", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.rating}/5 by {self.user} for {self.dealer}"


class CarMake(models.Model):
    name = models.CharField(max_length=80, unique=True)
    models = models.JSONField(default=list)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
