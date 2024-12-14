import requests
import logging
import sys
import time
from configparser import ConfigParser

def prompt():
  try:
    # Main Menu
    print("What would you like to do today? Enter command: ")
    print("   1 => search hotels")
    print("   2 => search flights")
    print("   3 => search attractions")
    print("   4 => search restaurants")
    print("   5 => end iTravel")
    cmd = input()
    return int(cmd)

  except Exception as e:
    print("ERROR: invalid input")
    return -1

# Calls web service
def get_web_service(url):
  try:
    retries = 0
    
    while True:
        response = requests.get(url)
        if response.status_code in [200, 400, 480, 481, 482, 500]:
            break
        retries += 1
        if retries < 3:
            time.sleep(retries)
            continue
        break

    return response

  except Exception as e:
    print("ERROR: get_web_service failed")
    return None
  
def get_details(baseurl, locationid):
    try:
        api = '/details/' + locationid
        url = baseurl + api
        res = get_web_service(url)
        
        if res.status_code == 200:
            pass
        else:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code == 500:
                body = res.json()
                print("Error message:", body)
            return

        # prints out the details
        body = res.json()
        details = body['details']
        if not details:
            print("No details found...")
            return
        print()
        print("Description:", details['description'])
        print("Web_url:", details['web_url'])
        print("Rating:", details['rating'])
        if details['price_level']:
            print("Price level:", details['price_level'])
        if details['hours']:
            print("Hours:", details['hours']['weekday_text'])
        if details['cuisine']:
            cuisine = details['cuisine']
            print("Cuisine:", end=" ")
            for i in range(len(cuisine)-1):
                print(cuisine[i]['localized_name'], end=", ")
            print(cuisine[-1]['localized_name']) # formatted
        if details['email']:
            print("Email:", details['email'])
        if details['phone']:
            print("Phone:", details['phone'])
        print()
        return
    except: 
        print("ERROR: something went wrong when searching for details")
    

# Search for hotels in given city
def hotels(baseurl):
    try:
        # Get user input city
        print("Which city are you looking to search for hotels? Enter city name: ")
        city = input()

        while not city:
           print("Oops! We didn't get that. Please try again: ")
           city = input()

        # Call web service
        api = '/hotels?destination=' + city
        url = baseurl + api
        res = get_web_service(url)

        if res.status_code == 200:
            pass
        else:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code == 500:
                body = res.json()
                print("Error message:", body)
            return

        body = res.json()
        hotels = body["hotels"]
        locationids = []
        if not hotels or len(hotels) == 0:
           print("No hotels found...")
        else:
            print("Found!")
            i = 1
            for hotel in hotels:
                line = str(i) + ". " + hotel["name"]
                print(line)
                print("Address:", hotel["address"]["address_string"])
                i += 1
                locationids.append(hotel["location_id"])
        
        print()
        # Learn more details
        print("Would you like to learn more about any of the locations? Enter Y or n: ")
        answer = input()
        while answer != "Y" and answer != "n":
            print("Invalid input! Please try again (Y/n): ")
            answer = input()
        if answer == "n":
            print()
            return
        
        # Get location id and call details()
        print("Which hotel would you like to dive deeper into? Enter index (1-10): ")
        answer = int(input())
        while answer <= 0 or answer > 10:
            print("Invalid index! Please try again: ")
            answer = int(input())
        get_details(baseurl, locationids[answer-1])
        return
    except:
       print("ERROR: something went wrong when searching for hotels")

def flights(baseurl):
    try:
        # Get origin airport
        print("Which airport are you flying from? Enter airport 3-digit IATA code (Ex: JFK = John F. Kennedy Airport): ")
        origin = input()
        while not origin:
           print("Oops! We didn't get that. Please try again: ")
           origin = input()
        
        # Get destination airport
        print("Which airport are you flying to? Enter airport 3-digit IATA code (Ex: JFK = John F. Kennedy Airport): ")
        destination = input()
        while origin == destination:
           print("Oops! Origin airport and destination airport can't be the same. Please try again: ")
           destination = input()
        while not destination:
           print("Oops! We didn't get that. Please try again: ")
           destination = input()

        # Call web service
        api = '/flights?origin=' + origin + '&destination=' + destination
        url = baseurl + api
        res = get_web_service(url)

        if res.status_code == 200:
            pass
        else:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code == 500:
                body = res.json()
                print("Error message:", body)
            return

        body = res.json()
        flights = body["flights"]
        if not flights or len(flights) == 0:
           print("No flights found...")
        else:
            print("Found!")
            i = 1
            for flight in flights:
                line = str(i) + ". " + flight["airline"]
                print(line)
                print("Flight:", flight["flight"])
                print("Departure Time", flight["departure time"])
                print("Departure Time Zone", flight["departure timezone"])
                print("Arrival Time", flight["arrival time"])
                print("Arrival Time Zone", flight["arrival timezone"])
                i += 1
        print()
        return
    except:
       print("ERROR: something went wrong when searching for flights")

def attractions(baseurl):
    try:
        # Get user input city
        print("Which city are you looking to search for attractions? Enter city name: ")
        city = input()

        while not city:
           print("Oops! We didn't get that. Please try again: ")
           city = input()

        # Call web service
        api = '/attractions?destination=' + city
        url = baseurl + api
        res = get_web_service(url)

        if res.status_code == 200:
            pass
        else:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code == 500:
                body = res.json()
                print("Error message:", body)
            return

        body = res.json()
        attractions = body["attractions"]
        locationids = []
        if not attractions or len(attractions) == 0:
           print("No attractions found...")
        else:
            print("Found!")
            i = 1
            for attraction in attractions:
                line = str(i) + ". " + attraction["name"]
                print(line)
                print("Address:", attraction["address"]["address_string"])
                i += 1
                locationids.append(attraction["location_id"])
        
        print()
        # Learn more details
        print("Would you like to learn more about any of the locations? Enter Y or n: ")
        answer = input()
        while answer != "Y" and answer != "n":
            print("Invalid input! Please try again (Y/n): ")
            answer = input()
        if answer == "n":
            print()
            return
        
        # Get location id and call details()
        print("Which attraction would you like to dive deeper into? Enter index (1-10): ")
        answer = int(input())
        while answer <= 0 or answer > 10:
            print("Invalid index! Please try again: ")
            answer = int(input())
        get_details(baseurl, locationids[answer-1])
        return
    except:
       print("ERROR: something went wrong when searching for attractions")

def restaurants(baseurl):
    try:
        # Get user input city
        print("Which city are you looking to search for restaurants? Enter city name: ")
        city = input()

        while not city:
           print("Oops! We didn't get that. Please try again: ")
           city = input()

        # Call web service
        api = '/restaurants?destination=' + city
        url = baseurl + api
        res = get_web_service(url)

        if res.status_code == 200:
            pass
        else:
            # failed:
            print("Failed with status code:", res.status_code)
            print("url: " + url)
            if res.status_code == 500:
                body = res.json()
                print("Error message:", body)
            return

        body = res.json()
        restaurants = body["restaurants"]
        locationids = []
        if not restaurants or len(restaurants) == 0:
           print("No restaurants found...")
        else:
            print("Found!")
            i = 1
            for restaurant in restaurants:
                line = str(i) + ". " + restaurant["name"]
                print(line)
                print("Address:", restaurant["address"]["address_string"])
                i += 1
                locationids.append(restaurant["location_id"])
        
        print()
        # Learn more details
        print("Would you like to learn more about any of the locations? Enter Y or n: ")
        answer = input()
        while answer != "Y" and answer != "n":
            print("Invalid input! Please try again (Y/n): ")
            answer = input()
        if answer == "n":
            print()
            return
        
        # Get location id and call details()
        print("Which attraction would you like to dive deeper into? Enter index (1-10): ")
        answer = int(input())
        while answer <= 0 or answer > 10:
            print("Invalid index! Please try again: ")
            answer = int(input())
        get_details(baseurl, locationids[answer-1])
        return
    except:
       print("ERROR: something went wrong when searching for restaurants")

#
# MAIN FUNCTION
#
try:
    print()
    print('#################################')
    print('#####  WELCOME TO ITRAVEL!  #####')
    print('#################################')

    favorites = {}
    sys.tracebacklimit = 0
    config_file = 'client-config.ini'

    configur = ConfigParser()
    configur.read(config_file)
    baseurl = configur.get('client', 'webservice')

    lastchar = baseurl[len(baseurl) - 1]
    if lastchar == "/":
        baseurl = baseurl[:-1]

    print()
    cmd = prompt()

    while cmd != 5:
        if cmd == 1:
            hotels(baseurl)
        elif cmd == 2:
            flights(baseurl)
        elif cmd == 3:
            attractions(baseurl)
        elif cmd == 4:
            restaurants(baseurl)
        else:
            print("Unknown command! Please try again: ")
        cmd = prompt()

    print()
    print('** Thank you for using iTravel! **')
    sys.exit(0)

except Exception as e:
    logging.error("ERROR: main function failed:")
    logging.error(e)
    sys.exit(0)
