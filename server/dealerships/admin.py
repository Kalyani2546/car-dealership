from django.contrib import admin

from .models import CarMake, Dealer, Review


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "phone")
    list_filter = ("state",)
    search_fields = ("name", "city", "state")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("dealer", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("name",)
