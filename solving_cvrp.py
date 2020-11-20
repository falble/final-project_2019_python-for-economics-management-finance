# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 22:35:02 2019

@author: Falble

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Albertini Francesco - 3029229
Contini Arnaldo - 3014053
"""

import call_distance_matrix_api as mtrx
import clean_csv as clean


from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


input_number = input('Enter number of vehicles: ')
number = int(input_number)

input_capacity = input('Enter vehicle capacity: ')
single_capacity = int(input_capacity)

capacity = []

for i in range(number):
    capacity.append(single_capacity)
    
# CREATE THE DATA
def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = mtrx.create_distance_matrix(mtrx.create_data())    
    data['demands'] = clean.demands
    # Each location has a demand corresponding to the quantity—for example, 
    # weight or volume—of the item to be picked up.
    data['vehicle_capacities'] = capacity
    # Each vehicle has a capacity: the maximum quantity that the vehicle can hold. 
    # As a vehicle travels along its route, the total quantity of the items it is carrying 
    # can never exceed its capacity.
    data['num_vehicles'] = number
    data['depot'] = 0
    return data

# ADD THE SOLUTION PRINTER
    # the solution printer displays all the route, along with its CUMULATIVE LOADS:
    # the total amount the vehicle is carrying at stop on its routes.
def print_solution(data, manager, routing, assignment):
    """Prints assignment on console."""
    total_distance = 0
    total_load = 0
    # setting the route for each vehicle 
    file = open('plan_outputGLS.txt','w')
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(
            manager.IndexToNode(index), route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        file.write(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))
    file.write('Total distance of all routes: {}m'.format(total_distance))
    file.write('Total load of all routes: {}'.format(total_load))
    file.close()

# NB the main function is very similar to the one of VRP, but also adds the DEMAND 
# and CAPACITY DIMENSION 
def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

#  ADD THE DISTANCE CALLBACK
    # ADD THE DEMAND CALLBACK AND CAPACITY COSTRAINTS
    # In addition to the distance callback, the solver also requires a demand callback, 
    # which returns the demand at each location, and a dimension for the capacity constraints.
    
    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]
   
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

#!!! NB
    # Unlike the distance callback, which takes a pair of locations as inputs, 
    # the demand callback only depends on the location (from_node) of the delivery.
    # The code also creates a dimension for capacities, we use the AddDimensionWithVehicleCapacity method, 
    # which takes a vector of capacities.
    # Since all the vehicle capacities in this example are the same, you could use the the 
    # AddDimension method, which takes a single upper bound for all vehicle quantities. 
    # But AddDimensionWithVehicleCapacity handles the more general case in which different 
    # vehicles have different capacities.
    
    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack, modify it if you accept unmet demand
        data['vehicle_capacities'],  # vehicle maximum capacities set by the user
        True,  # start cumul to zero
        'Capacity')
    
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

    # Search status 
    print('\n')
    solver_index = routing.status()
    description = ['ROUTING_NOT_SOLVED','ROUTING_SUCCESS','ROUTING_FAIL',
                   'ROUTING_FAIL_TIMEOUT','ROUTING_INVALID']
    print("Solver status:",description[solver_index],'\n')
    
    # Print solution on console.
    if assignment:
        print_solution(data, manager, routing, assignment)


if __name__ == '__main__':
    main()
    
"""
For each location on a route, the output shows:
- The index of the location.
- The total load carried by the vehicle when it departs the location.
"""