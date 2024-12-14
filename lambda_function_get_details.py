import json
import requests
import os

def lambda_handler(event, context):
    # Get the destination from the event
    if "locationid" in event:
        locationid = int(event['locationid'])
    elif "pathParameters" in event:
        if "locationid" in event['pathParameters']:
            locationid = int(event['pathParameters']["locationid"])
    
    if not locationid:
        return {
            "statusCode": 400,
            "body": json.dumps({"Error": "Invalid Input!"})
        }
    
    # TripAdvisor API endpoint and key
    tripadvisor_base_url = f"https://api.content.tripadvisor.com/api/v1/location/{locationid}/details?key=TRIP_ADVISOR_API_KEY&language=en"
    api_key = os.environ.get("TRIP_ADVISOR_API_KEY")
    
    try:
        # Make a request to the TripAdvisor API
        response = requests.get(tripadvisor_base_url)
        response.raise_for_status()
        data = response.json()
        
        # Extract details
        details = {
                "description": data.get("description"),
                "web_url": data.get("web_url"),
                "rating": data.get("rating"),
                "hours": data.get("hours"),
                "cuisine": data.get("cuisine"),
                "price_level": data.get("price_level"),
                "email": data.get("email"),
                "phone": data.get("phone")}
        
        return {
            "statusCode": 200,
            "body": json.dumps({"locationid": locationid, "details": details})
        }
    except requests.RequestException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to fetch data from TripAdvisor", "details": str(e)})
        }
