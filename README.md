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
3. pip install -r requirements.txt
4. ./manage.py runserver

# API
The server offers an RESFUL web api to store and retrieve sensor signals and actuation events: POST to create, PUT to update, DELETE to DELETE.  You can look at  /vm/data_connection.py to see examples of calling the server.

Users register a computer instance before using most commands.  Registration returns a local_computer object with an id that is used to identfiy other API requests.
