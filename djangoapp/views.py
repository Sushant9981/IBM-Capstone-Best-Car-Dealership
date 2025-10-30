from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt
import logging
import json

from .models import CarMake, CarModel, LocalReview
from .populate import initiate
from .restapis import get_request, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)

# -------------------- AUTHENTICATION --------------------


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]
    try:
        User.objects.get(username=username)
        return JsonResponse(
            {"userName": username, "error": "Already Registered"}
        )
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})


# -------------------- DEALERSHIPS --------------------


def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": [dealership]})
    return JsonResponse({"status": 400, "message": "Bad Request"})


# -------------------- REVIEWS --------------------


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        external_reviews = get_request(endpoint)
        local_reviews = LocalReview.objects.filter(dealer_id=dealer_id)

        all_reviews = list(external_reviews)
        for review in local_reviews:
            all_reviews.append(
                {
                    "name": review.name,
                    "review": review.review,
                    "car_make": review.car_make,
                    "car_model": review.car_model,
                    "car_year": review.car_year,
                    "sentiment": review.sentiment,
                }
            )

        return JsonResponse({"status": 200, "reviews": all_reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


@csrf_exempt
def add_review(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            dealership = data.get("dealership")
            review = data.get("review")
            purchase_date = data.get("purchase_date")
            car_make = data.get("car_make")
            car_model = data.get("car_model")
            car_year = data.get("car_year")

            try:
                response = post_review(data)
                print("Cloud review post response:", response)
            except Exception as api_error:
                print(f"Remote post_review() failed: {api_error}")

            LocalReview.objects.create(
                dealer_id=dealership,
                name=name,
                review=review,
                purchase_date=purchase_date,
                car_make=car_make,
                car_model=car_model,
                car_year=car_year,
                sentiment="neutral",
            )
            return JsonResponse(
                {"status": 200, "message": "Review saved successfully"}
            )
        except Exception as e:
            print(f"Error posting review: {e}")
            return JsonResponse(
                {"status": 500, "message": "Error saving review"}
            )
    return JsonResponse({"status": 405, "message": "Method Not Allowed"})


# -------------------- CARS --------------------


def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related("car_make")
    cars = [
        {"CarModel": cm.name, "CarMake": cm.car_make.name}
        for cm in car_models
    ]
    return JsonResponse({"CarModels": cars})
