import json
import requests
import os

def lambda_handler(event, context):
    # Get origin and destination from the event
    if "origin" in event or "destination" in event:
        if "origin" in event:
            origin = event["origin"]
        if "destination" in event:
            destination = event["destination"]
    elif "queryStringParameters" in event:
        if "origin" in event["queryStringParameters"]:
            origin = event["queryStringParameters"]["origin"]
        if "destination" in event["queryStringParameters"]:
            destination = event["queryStringParameters"]["destination"]
    
    if not origin or not destination:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Invalid Input!"
            })
        }
    
    # Flight API base url and key
    base_url = "https://api.aviationstack.com/v1/flights?access_key=AVIATION_STACK_API_KEY"
    api_key = os.environ.get("AVIATION_STACK_API_KEY")
    
    # Build request parameters
    params = {
        "access_key": api_key,
        "dep_iata": origin,
        "arr_iata": destination
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract flight details
        flights = [
            {
                "airline": flight.get("airline")['name'],
                "flight": flight.get("flight")['iata'],
                "departure time": flight.get("departure")["estimated"],
                "departure timezone": flight.get("departure")["timezone"],
                "arrival time": flight.get("arrival")["estimated"],
                "arrival timezone": flight.get("arrival")["timezone"],
            }
            for flight in data.get("data", [])
        ]
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "origin": origin,
                "destination": destination,
                "flights": flights
            })
        }
    except requests.RequestException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Failed to fetch flight data",
                "details": str(e)
            })
        }
