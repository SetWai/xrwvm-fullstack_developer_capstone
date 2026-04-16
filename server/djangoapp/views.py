from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

# Logger instance
logger = logging.getLogger(__name__)


def get_cars(request):
    """Fetch all car models and makes."""
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": cm.name, "CarMake": cm.car_make.name}
            for cm in car_models]
    return JsonResponse({"CarModels": cars})


@csrf_exempt
def login_user(request):
    """Handle user login."""
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"userName": username, "status": "Failed"})


def logout_request(request):
    """Handle user logout."""
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    """Handle user registration."""
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"userName": username, "error": "Already Registered"}
        )

    user = User.objects.create_user(
        username=username, first_name=first_name,
        last_name=last_name, password=password, email=email
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


def get_dealerships(request, state="All"):
    """Fetch dealerships by state."""
    endpoint = ("/fetchDealers" if state == "All"
                else f"/fetchDealers/{state}")
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    """Fetch reviews for a specific dealer."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)

    if reviews:
        for review_detail in reviews:
            review_text = review_detail.get('review', '')
            response = analyze_review_sentiments(review_text)

            if response and 'sentiment' in response:
                review_detail['sentiment'] = response['sentiment']
            else:
                review_detail['sentiment'] = 'neutral'

    return JsonResponse({"status": 200, "reviews": reviews})


@csrf_exempt
def add_review(request):
    """Post a new review."""
    if not request.user.is_authenticated:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    try:
        data = json.loads(request.body)
        post_review(data)
        return JsonResponse({"status": 200})
    except Exception as e:
        logger.error(f"Error in posting review: {e}")
        return JsonResponse(
            {"status": 401, "message": "Error in posting review"}
        )
