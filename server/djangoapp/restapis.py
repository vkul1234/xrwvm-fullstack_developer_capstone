import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define backend and sentiment analyzer URLs with default fallbacks
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

# Function to send a GET request to the backend
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    request_url = f"{backend_url}{endpoint}?{params}"

    print(f"GET from {request_url}")
    try:
        # Send GET request
        response = requests.get(request_url)
        return response.json()
    except requests.RequestException as err:
        # Handle network exceptions
        print(f"Network exception occurred: {err}")

# Function to analyze review sentiments by making a request to the sentiment analyzer service
def analyze_review_sentiments(text):
    request_url = f"{sentiment_analyzer_url}/analyze/{text}"
    try:
        # Send GET request to sentiment analyzer
        response = requests.get(request_url)
        return response.json()
    except requests.RequestException as err:
        # Handle network exceptions
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")

# Function to post a review to the backend
def post_review(data_dict):
    request_url = f"{backend_url}/insert_review"
    try:
        # Send POST request with the review data
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except requests.RequestException as err:
        # Handle network exceptions
        print(f"Network exception occurred: {err}")
