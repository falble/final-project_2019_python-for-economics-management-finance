# final-project_2019_python-for-economics-management-finance
Final Project for an elective course of my bachelor degree in Business Administration and Management. 

##### Francesco Albertini – 3029229
##### Arnaldo Contini – 3014053

## CAPACITATED VEHICLE ROUTING PROBLEM

### PRESENTATION:

The Capacitated Vehicle Routing Problem (CVRP) is a vehicle routing problem in which a fleet of vehicles, with equal limited capacity, must service customers (pick up items) with known demand at various locations. Empty vehicles must start their routes from the deposit, load items and bring them back to the starting point, and each customer can be served by only one vehicle. Finally, the demand of each client needs to be satisfied. Therefore, the cumulative capacity of all vehicles must be greater or equal than the cumulative demand of all clients.

The problem is to find an assignment of routes to vehicles that has the shortest total distance (intended as the lowest cost), and such that the total amount a vehicle is carrying never exceeds its capacity. Thus, the goal of our project is to provide firms facing this problem with a useful tool to minimize their transportation costs and increase efficiency.

We have imported (and then modified according to our needs) the main program from Google OR-Tools, an open source library for linear and non-linear optimization problems. Moreover, we have used the csv library in python, to read and work on the dataset, and the Google Distance Matrix API, to create the distance matrix for any set of locations.
Our intended field of application is clearly operations research. In order to evaluate our code, we have taken data from a real relocation firm which has to pick-up electric scooters at different locations and bring them back to the deposit to charge them. They need an alternative way to find the best path for their trucks. As of today, their only available tool is Google Maps, which has a number of limitations; in particular, you cannot insert more than 10 addresses, the sequence of locations must be predefined by the user and capacity constraint cannot be considered.
