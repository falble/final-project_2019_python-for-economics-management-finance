# final-project_2019_python-for-economics-management-finance
Final Project for an elective course of my bachelor degree in Business Administration and Management. 

#### Francesco Albertini – 3029229
#### Arnaldo Contini – 3014053

##### NB. unfortunately this project requires a Google API key in order to use the Cloud Platform.

## CAPACITATED VEHICLE ROUTING PROBLEM

### PRESENTATION:

The Capacitated Vehicle Routing Problem (CVRP) is a vehicle routing problem in which a fleet of vehicles, with equal limited capacity, must service customers (pick up items) with known demand at various locations. Empty vehicles must start their routes from the deposit, load items and bring them back to the starting point, and each customer can be served by only one vehicle. Finally, the demand of each client needs to be satisfied. Therefore, the cumulative capacity of all vehicles must be greater or equal than the cumulative demand of all clients.

The problem is to find an assignment of routes to vehicles that has the shortest total distance (intended as the lowest cost), and such that the total amount a vehicle is carrying never exceeds its capacity. Thus, the goal of our project is to provide firms facing this problem with a useful tool to minimize their transportation costs and increase efficiency.

We have imported (and then modified according to our needs) the main program from Google OR-Tools, an open source library for linear and non-linear optimization problems. Moreover, we have used the csv library in python, to read and work on the dataset, and the Google Distance Matrix API, to create the distance matrix for any set of locations.
Our intended field of application is clearly operations research. In order to evaluate our code, we have taken data from a real relocation firm which has to pick-up electric scooters at different locations and bring them back to the deposit to charge them. They need an alternative way to find the best path for their trucks. As of today, their only available tool is Google Maps, which has a number of limitations; in particular, you cannot insert more than 10 addresses, the sequence of locations must be predefined by the user and capacity constraint cannot be considered.

### INSTALLATION OF LIBRARIES:

If you already have Python 2.7 or 3.5+ installed (as well as the Python package manager, PIP), the easiest way to install OR-Tools is to write the following code in the anaconda prompt:
```
python -m pip install --upgrade --user ortools
```

### CONTENT OF THE REPOSITORY:

✓ Three python files: clean_csv.py, call_distance_matrix_api.py, solving_cvrp.py.
✓ Three examples: Milan.csv, Clients_1.csv, Clients_2.csv.

### USER MANUAL:

Firstly, you need an Internet connection. Then you have to open the 3 provided python files, and then create a dataset in excel with 3 characteristics (columns): location’s name (1st), customer’s address (2nd) and demand at that location (3rd). Addresses must be written as follows: street’s name, street’s number, city, province (e.g. “Via Olgia 18 Segrate MI”); it doesn’t matter if upper or lower case. If you want to change the order of columns, you just have to modify the numbers at lines 30-31-32 in the clean_csv file (0 = first column of the csv, 1 = second column and 2 = third column).
```
# filling the three different list reading the csv file    
with open(file,'r') as fi:
    reader = csv.reader(fi, delimiter = ';')
    header_row = next(reader)
    for row in reader:
        # modify the three numbers if you want change the csv variables order
        locations.append(row[0])
        dirty_addresses.append(row[1])
        demands.append(int(row[2]))
```
Save then the file in CSV UTF-8 (comma delimited) format in the same folder. Use the name you want for the file and insert it in line 21 in the clean_csv.
```
############################
## INSERT HERE THE  ########
## NAME OF CSV FILE ########
############################
file = 'Milan.csv'
```
In the same file, not in the csv, insert the deposit address at line 47 in the adequate form (e.g. “Via+Zenale+82+Garbagnate+Milanese+MI”).
```
#############################################
## INSERT HERE THE DEPOT ADDRESS ############
#############################################
depot = 'Via+Zenale+82+Garbagnate+Milanese+MI'
depot_load = 0
```
Finally, you have to insert your API key at line 32 of call_distance_matrix_api.py file.
```
def create_data():
  """Creates the data."""
  data = {}
  # this is the API key available signing in Google Cloud Platform
  data['API_key'] = # insert here your API_key
  data['addresses'] = clean.addresses
  return data
```
At this point, run the solving_cvrp.py file, pressing F5; the program will ask you to write the number and capacity of vehicles in the console.

Optional: To use a different search method, first solution strategy or local search strategy, check https://developers.google.com/optimization/routing/routing_options; insert the name of the search method at line 154 of solving_cvrp.py in uppercase and use underscores instead of spaces.
```
    # you can find other research method here:
    # https://developers.google.com/optimization/routing/routing_options
    
    # Setting first solution heuristic:
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
#    search_parameters.first_solution_strategy = (
#        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Setting metaheuristic search method:
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    # Setting time limit to the method
    search_parameters.time_limit.seconds = 30
    
    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)
```
Wait 30 seconds (if you want the program to try to find a better solution for a longer period of time modify the number at line 156 of solving_cvrp.py file) and you will find the optimal solution in the console. The meaning of solver status is the following:
➢ ROUTING_NOT_SOLVED: Problem not solved yet.
➢ ROUTING_SUCCESS: Problem solved successfully.
➢ ROUTING_FAIL: No solution found to the problem.
➢ ROUTING_FAIL_TIMEOUT: Time limit reached before finding a solution.
➢ ROUTING_INVALID: Model, model parameters, or flags are not valid.

For each location on a route, the output shows the index of the location and the total load carried by the vehicle when it departs the location. The program will automatically save the output as a txt file in the same folder.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0
