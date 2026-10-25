from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from dealerships.models import CarMake, Dealer, Review

DEALERS = [
    ("Sunflower Auto Center", "Topeka", "KS", "2100 SW Topeka Blvd", "66611", "785-555-0142"),
    ("Prairie Motors", "Wichita", "KS", "4820 East Kellogg Drive", "67218", "316-555-0196"),
    ("Crossroads Toyota", "Kansas City", "KS", "9330 State Avenue", "66112", "913-555-0118"),
    ("Lone Star Automotive", "Austin", "TX", "7400 Burnet Road", "78757", "512-555-0162"),
    ("Lakefront Auto Group", "Chicago", "IL", "1800 North Clybourn Avenue", "60614", "312-555-0130"),
    ("Evergreen Motors", "Seattle", "WA", "5200 Airport Way S", "98108", "206-555-0174"),
]
MAKES = {
    "Acura": ["Integra", "MDX", "RDX"],
    "BMW": ["3 Series", "5 Series", "X5"],
    "Chevrolet": ["Equinox", "Malibu", "Silverado"],
    "Ford": ["Bronco", "Escape", "F-150"],
    "Honda": ["Accord", "Civic", "CR-V"],
    "Toyota": ["Camry", "Corolla", "RAV4"],
}


class Command(BaseCommand):
    help = "Create the sample dealers and car makes used by the project."

    def handle(self, *args, **options):
        sample_user, _ = User.objects.get_or_create(
            username="sample-driver",
            defaults={"first_name": "Sample", "last_name": "Driver"},
        )
        sample_user.set_unusable_password()
        sample_user.save(update_fields=["password"])

        for name, city, state, address, zip_code, phone in DEALERS:
            dealer, _ = Dealer.objects.update_or_create(
                name=name,
                defaults={
                    "city": city,
                    "state": state,
                    "address": address,
                    "zip_code": zip_code,
                    "phone": phone,
                    "website": "",
                },
            )
            sample_review = {
                "Sunflower Auto Center": (5, "Sample review: The team was friendly and answered all my questions."),
                "Prairie Motors": (4, "Sample review: Helpful staff and a smooth visit from start to finish."),
                "Crossroads Toyota": (5, "Sample review: Excellent service and a welcoming showroom."),
            }.get(name)
            if sample_review:
                rating, text = sample_review
                Review.objects.get_or_create(
                    dealer=dealer,
                    user=sample_user,
                    review=text,
                    defaults={"rating": rating},
                )
        for name, models in MAKES.items():
            CarMake.objects.update_or_create(name=name, defaults={"models": models})
        self.stdout.write(self.style.SUCCESS("Sample dealerships and car makes are ready."))
