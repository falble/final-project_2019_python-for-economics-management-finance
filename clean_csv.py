# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 22:34:29 2019

@author: Falble

Albertini Francesco - 3029229
Contini Arnaldo - 3014053
"""

import csv

locations = []
dirty_addresses = []
demands = []

############################
## INSERT HERE THE  ########
## NAME OF CSV FILE ########
############################
file = 'Milan.csv'


# filling the three different list reading the csv file    
with open(file,'r') as fi:
    reader = csv.reader(fi, delimiter = ';')
    header_row = next(reader)
    for row in reader:
        # modify the three numbers if you want change the csv variables order
        locations.append(row[0])
        dirty_addresses.append(row[1])
        demands.append(int(row[2]))
        
        
#print(locations)
#print(dirty_addresses)
#print(demands)

# clean the addresses in an adequate form for the distance matrix API
addresses = []
for i in dirty_addresses:
    new = i.replace(' ','+')
    addresses.append(new)
    
#print(indirizzi)

#############################################
## INSERT HERE THE DEPOT ADDRESS ############
#############################################
depot = 'Via+Zenale+82+Garbagnate+Milanese+MI'
depot_load = 0

# adding the depot address to the addresses list in the first position    
addresses.insert(0,depot)
# adding depot demand (zero) in the demand list
demands.insert(0,depot_load)
# adding depot location in the location list
locations.insert(0,'Deposit')


# creating a txt file, in the same folder, to allow the user to check the addresses' form
with open('addresses.txt','w') as ind:
    for address in addresses:
        ind.write('%s\n' %address)

ind.close()