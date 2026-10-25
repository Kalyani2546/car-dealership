import json

from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import Dealer, Review


class DealershipApiTests(TestCase):
    def setUp(self):
        self.dealer = Dealer.objects.create(
            name="Sunflower Auto Center",
            city="Topeka",
            state="KS",
            address="2100 SW Topeka Blvd",
            zip_code="66611",
            phone="785-555-0142",
        )

    def test_state_filter_is_case_insensitive(self):
        response = self.client.get("/api/dealers/?state=ks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["state"] for item in response.json()], ["KS"])

    def test_review_submission_requires_login(self):
        response = self.client.post(
            "/api/reviews/",
            data=json.dumps({"dealer_id": self.dealer.id, "rating": 5, "review": "Excellent service"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_signed_in_user_can_post_and_read_review(self):
        user = User.objects.create_user(username="sam", password="local-test-password")
        self.client.force_login(user)
        response = self.client.post(
            "/api/reviews/",
            data=json.dumps({"dealer_id": self.dealer.id, "rating": 5, "review": "Fantastic services"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Review.objects.count(), 1)
        reviews = self.client.get(f"/api/dealers/{self.dealer.id}/reviews/")
        self.assertEqual(reviews.json()[0]["username"], "sam")

    def test_review_analyzer(self):
        response = self.client.post(
            "/api/analyze-review/",
            data=json.dumps({"review": "Fantastic services"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"label": "positive", "score": 1})

    def test_registration_creates_user_and_starts_session(self):
        response = self.client.post(
            "/api/register/",
            data=json.dumps({
                "username": "drivefan",
                "first_name": "Taylor",
                "last_name": "Brooks",
                "email": "taylor@example.com",
                "password": "Swerve-into-a-new-drive-983!",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["username"], "drivefan")
        self.assertTrue(self.client.get("/api/me/").json()["authenticated"])

    def test_about_and_contact_pages_render(self):
        self.assertContains(self.client.get("/about/"), "About Cars Dealership")
        contact = self.client.get("/contact/")
        self.assertContains(contact, "Contact Us")
        self.assertContains(contact, 'href="/static/site.css"')

    def test_mutating_api_requires_csrf_and_accepts_cookie_token(self):
        client = Client(enforce_csrf_checks=True)
        url = "/api/analyze-review/"
        body = json.dumps({"review": "Fantastic services"})
        denied = client.post(url, data=body, content_type="application/json")
        self.assertEqual(denied.status_code, 403)
        client.get("/api/csrf/")
        token = client.cookies["csrftoken"].value
        accepted = client.post(
            url,
            data=body,
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(accepted.status_code, 200)
