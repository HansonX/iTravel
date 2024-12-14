import json
import requests
import os

def lambda_handler(event, context):
    # Get the destination from the event
    if "destination" in event:
      destination = event["destination"]
    elif "queryStringParameters" in event:
      if "destination" in event["queryStringParameters"]:
        destination = event["queryStringParameters"]["destination"]
    
    if not destination:
        return {
            "statusCode": 400,
            "body": json.dumps({"Error": "Invalid Input!"})
        }
    
    # TripAdvisor API endpoint and key
    tripadvisor_base_url = "https://api.content.tripadvisor.com/api/v1/location/search?key=TRIP_ADVISOR_API_KEY&language=en"
    api_key = os.environ.get("TRIP_ADVISOR_API_KEY")
    
    # Build request parameters
    params = {
        "searchQuery": destination,
        "category": "restaurants"
    }
    
    try:
        # Make a request to the TripAdvisor API
        response = requests.get(tripadvisor_base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        restaurants = [
            {
                "location_id": restaurant.get("location_id"),
                "name": restaurant.get("name"),
                "address": restaurant.get("address_obj"),
            }
            for restaurant in data.get("data", [])
        ]
        
        return {
            "statusCode": 200,
            "body": json.dumps({"destination": destination, "restaurants": restaurants})
        }
    except requests.RequestException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to fetch data from TripAdvisor", "details": str(e)})
        }