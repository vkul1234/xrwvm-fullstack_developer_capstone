from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_user` view to handle sign-in requests
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']

    user = authenticate(username=username, password=password)
    data = {"userName": username}

    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# Create a `logout_request` view to handle sign-out requests
def logout_request(request):
    username = request.user.username
    logout(request)
    data = {"userName": username}
    return JsonResponse(data)


# Create a `registration` view to handle sign-up requests
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    try:
        User.objects.get(username=username)
        data = {"userName": username, "error": "Already Registered"}
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, 
                                        first_name=first_name, 
                                        last_name=last_name, password=password, 
                                        email=email)
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}

    return JsonResponse(data)


# Create a view to get car models
def get_cars(request):
    if not CarMake.objects.exists():
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": car_model.name, 
             "CarMake": car_model.car_make.name} for car_model in car_models]

    return JsonResponse({"CarModels": cars})


# Update `get_dealerships` to render list of dealerships, all by default, or filter by state
def get_dealerships(request, state="All"):
    if state == "All":
    endpoint = "/fetchDealers"
    
    else:
    endpoint = f"/fetchDealers/{state}"

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Create a `get_dealer_reviews` view to render dealer reviews
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']

        return JsonResponse({"status": 200, "reviews": reviews})

    return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `get_dealer_details` view to render dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})

    return JsonResponse({"status": 400, "message": "Bad Request"})


# Create an `add_review` view to submit a review
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            print(e)
            return JsonResponse({"status": 401, 
                                 "message": "Error in posting review"})

    return JsonResponse({"status": 403, "message": "Unauthorized"})
