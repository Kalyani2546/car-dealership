import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .models import CarMake, Dealer, Review
from .sentiment import analyze_sentiment
from .serializers import dealer_data, review_data


def read_json(request):
    try:
        data = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


@require_GET
@ensure_csrf_cookie
def csrf_token(_request):
    return JsonResponse({"detail": "CSRF cookie set"})


@require_POST
def register(request):
    data = read_json(request)
    if data is None:
        return JsonResponse({"error": "Request body must be a JSON object."}, status=400)

    fields = ("username", "first_name", "last_name", "email", "password")
    if any(not isinstance(data.get(field), str) for field in fields):
        return JsonResponse({"error": "All five registration fields must be text."}, status=400)
    username = data["username"].strip()
    first_name = data["first_name"].strip()
    last_name = data["last_name"].strip()
    email = data["email"].strip()
    password = data.get("password", "")
    if not all((username, first_name, last_name, email, password)):
        return JsonResponse({"error": "All five registration fields are required."}, status=400)
    if len(username) > 150 or len(password) > 128:
        return JsonResponse({"error": "Username or password exceeds the supported length."}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "That username is already registered."}, status=409)

    user = User(username=username, first_name=first_name, last_name=last_name, email=email)
    try:
        validate_password(password, user=user)
    except ValidationError as error:
        return JsonResponse({"error": error.messages}, status=400)
    user.set_password(password)
    try:
        user.full_clean(exclude=["password"])
    except ValidationError as error:
        return JsonResponse({"error": error.messages}, status=400)
    user.save()
    login(request, user)
    return JsonResponse({"username": user.get_username(), "authenticated": True}, status=201)


@require_POST
def login_user(request):
    data = read_json(request)
    if data is None:
        return JsonResponse({"error": "Request body must be a JSON object."}, status=400)
    user = authenticate(request, username=data.get("username", ""), password=data.get("password", ""))
    if user is None:
        return JsonResponse({"error": "Invalid username or password."}, status=400)
    login(request, user)
    return JsonResponse({"username": user.get_username(), "authenticated": True})


@require_POST
def logout_user(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You are not logged in."}, status=401)
    logout(request)
    return JsonResponse({"detail": "Successfully logged out.", "authenticated": False})


@require_GET
def current_user(request):
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False, "username": None})
    return JsonResponse({"authenticated": True, "username": request.user.get_username()})


@require_GET
def dealers(request):
    queryset = Dealer.objects.all()
    state = request.GET.get("state", "").strip().upper()
    if state:
        if len(state) != 2 or not state.isalpha():
            return JsonResponse({"error": "State must be a two-letter abbreviation."}, status=400)
        queryset = queryset.filter(state=state)
    return JsonResponse([dealer_data(item) for item in queryset], safe=False)


@require_GET
def dealer_detail(_request, dealer_id):
    try:
        dealer = Dealer.objects.get(pk=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({"error": "Dealership not found."}, status=404)
    return JsonResponse(dealer_data(dealer))


@require_GET
def dealer_reviews(_request, dealer_id):
    if not Dealer.objects.filter(pk=dealer_id).exists():
        return JsonResponse({"error": "Dealership not found."}, status=404)
    reviews = Review.objects.filter(dealer_id=dealer_id).select_related("user")
    return JsonResponse([review_data(item) for item in reviews], safe=False)


@require_POST
def create_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Sign in to post a review."}, status=401)
    data = read_json(request)
    if data is None:
        return JsonResponse({"error": "Request body must be a JSON object."}, status=400)
    try:
        dealer = Dealer.objects.get(pk=int(data.get("dealer_id")))
        rating = int(data.get("rating"))
    except (Dealer.DoesNotExist, TypeError, ValueError):
        return JsonResponse({"error": "A valid dealer_id and rating are required."}, status=400)
    text = str(data.get("review", "")).strip()
    if rating < 1 or rating > 5:
        return JsonResponse({"error": "Rating must be between 1 and 5."}, status=400)
    if not text or len(text) > 2000:
        return JsonResponse({"error": "Review must contain 1–2000 characters."}, status=400)
    review = Review.objects.create(dealer=dealer, user=request.user, rating=rating, review=text)
    return JsonResponse(review_data(review), status=201)


@require_GET
def car_makes(_request):
    return JsonResponse(
        [{"id": make.id, "name": make.name, "models": make.models} for make in CarMake.objects.all()],
        safe=False,
    )


@require_POST
def analyze_review(request):
    data = read_json(request)
    if data is None:
        return JsonResponse({"error": "Request body must be a JSON object."}, status=400)
    text = str(data.get("review", "")).strip()
    if not text or len(text) > 2000:
        return JsonResponse({"error": "Review text must contain 1–2000 characters."}, status=400)
    return JsonResponse(analyze_sentiment(text))
