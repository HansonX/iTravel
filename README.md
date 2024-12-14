# iTravel
A cloud-native application that allows users to search for hotels, restaurants, attractions, and real-time flights to help plan their vacation. This application consists of 5 lambda functions. 4 access the TripAdvisor API, and 1 accesses the AviationStack API. 

# Features:
- search-hotels: based on a user-specified location, print 10 hotels in that location
- search-restaurants: based on a user-specified location, print 10 restaurants in that location
- search-attractions: based on a user-specified location, print 10 attractions in that location
- search-flights: based on an origin airport IATA code and a destination airport IATA code, print real-time flights that are available
- get-details: based on a TripAdvisor location ID, print details regarding the location

# Client:
The client-side app runs in the terminal. When the client runs the main.py file and starts the application, a welcome message is printed. The client is then brought to the main menu, where they can choose to run any of the features or end iTravel. If the client decides to end iTravel, a thank you message is printed, and the application is shut down.

The AWS API Gateway is responsible for receiving client requests and directing them to the appropriate AWS Lambda function service. The API Gateway has 5 resources and 1 GET request method within each resource. The invoke URL for the API Gateway is stored in client-config.ini and used when the application starts. Each lambda function has a layer that contains json and requests libraries, allowing them to access external APIs and send JSON files.
