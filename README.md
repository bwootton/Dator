# Dator - Data Aggregation for Robots
Data aggregation and control program selection for groups of robots

Dator is a lightweight data aggregation platform for groups of robots.  It's built to address the following needs:

* Aggregation of data from multiple robots to a central platform.
* HTTP(S) command polling and data push from robots on private networks to a centralized platform, avoiding the need to bridge into the local robot's network to control and anlyze data.
* RESTful access of aggregated data for simple data anlaysis and command generation by remote systems.
* Management of data sets across multiple hardware and software modifications.
* **Optionally:** Easy iteration of program update, deploy and test to a group of robots.

The main role of the platform is to provide a standard way to record data and actuation events from one or more local computers (robots) for later analysis of robot performance and simulation of new control regimens.

# Setup
The application is a standard Django Server 1.8 application using Python 2.7.x.   If you have python 2.7 installed, you should be able to:

1. Clone the repository to a local directory
2. Install PIP if you haven't already.
3. **pip install -r requirements.txt**
4. **./manage.py runserver**

# API
The server offers an RESFUL web api to store and retrieve sensor signals and actuation events: 

* GET to view either a list **e.g. GET /api/v1/event/** or a single instance **e.g. GET /api/v1/event/15/** of an object 
* POST to create an objects, **e.g. POST /api/v1/event/**
* PUT to update, **e.g. PUT /api/v1/event/1/** 
* DELETE to delete and obect **e.g. DELETE /api/v1/event/1/**.  
 
You can look at  /vm/data_connection.py to see examples of calling the server.

Users register a computer instance before using most commands.  Registration returns a local_computer object with an id that is used to identfiy other API requests.
## Endpoints
### /api/v1/register/
#### Filter parameters

#### Fields

