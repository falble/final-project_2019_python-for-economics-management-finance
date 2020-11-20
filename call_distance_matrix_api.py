# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 22:35:18 2019

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

import clean_csv as clean
import json
import urllib.request as ur


def create_data():
  """Creates the data."""
  data = {}
  # this is the API key available signing in Google Cloud Platform
  data['API_key'] = # insert here your API_key
  data['addresses'] = clean.addresses
  return data


def create_distance_matrix(data):
  addresses = data["addresses"]
  API_key = data["API_key"]
  # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
  max_elements = 100
  num_addresses = len(addresses) 
  # maximum number of rows that can be computed per request
  max_rows = max_elements // num_addresses
  # num_address = q * max_rows + r
  q, r = divmod(num_addresses, max_rows)
  dest_addresses = addresses
  distance_matrix = []
  # Send q requests, returning max_rows rows per request.
  for i in range(q):
    origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)

  # Get the remaining remaining r rows, if necessary.
  if r > 0:
    origin_addresses = addresses[q * max_rows: q * max_rows + r]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)
  return distance_matrix


def send_request(origin_addresses, dest_addresses, API_key):
  """ Build and send request for the given origin and destination addresses."""
  def build_address_str(addresses):
    # Build a pipe-separated string of addresses
    address_str = ''
    for i in range(len(addresses) - 1):
      address_str += addresses[i] + '|'
    address_str += addresses[-1]
    return address_str
    
  # A Distance Matrix API request is a long string containing the following:
  # API address, the end of the request 'json' asks the response in JSON.
  # request option 'units=imperial' sets the language of the response to English
  request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
  origin_address_str = build_address_str(origin_addresses)
  dest_address_str = build_address_str(dest_addresses)
  # assembling the parts of the request described above, and sends the request
  request = request + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key
  jsonResult = ur.urlopen(request).read()
  # converting the raw result to a Python object
  response = json.loads(jsonResult)
  return response

# the following builds rows of the distance matrix, using the response returned by 
# the send_request function
def build_distance_matrix(response):
  distance_matrix = []
  for row in response['rows']:
    row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
    distance_matrix.append(row_list)
  return distance_matrix

def main():
  """Entry point of the program"""
  # Create the data.
  data = create_data()
  addresses = data['addresses']
  API_key = data['API_key']
  distance_matrix = create_distance_matrix(data)
  print(distance_matrix)
  # creating a txt file to let the user store the distance matrix in the folder
  with open('distance_matrix_prova1.txt','w') as mtx:
      for row in distance_matrix:
          mtx.write('%s\n' %row)
      
      
if __name__ == '__main__':
  main()