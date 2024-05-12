# Imports
import numpy as np
import pandas as pd
import tensorflow as tf
import string


#Reading the data
data = pd.read_csv('NewCity/cities.py')
cities = data['city'].tolist()

# Manipulating the data
for i in range(len(cities) - 1, -1, -1):  # iterate in reverse order
    if not cities[i].isalpha():
        cities.pop(i)  # remove item by index
    else:
        cities[i] = cities[i].lower()
letters = string.ascii_lowercase
for i in range(len(cities)-1,-1,-1):
    for j in cities[i]:
        if j not in letters:
            cities.pop(i)
            break
        else:
            continue
for i in range(len(cities)-1, -1 , -1):
    cities[i] = '.'+ cities[i] + '.'

# Initiate an  adjacency LIKE matrix
matrix = np.zeros((27, 27))

#Create a mapping from letters to integers
ltoi = {}
for i in range(len(letters)):
    ltoi[letters[i]] = i
ltoi['.']=26

#Create a mapping from integers to letters
itol = {}
for i in range(len(letters)):
    itol[i] = letters[i]
itol[26] = '.'

#First letter - row second letter - column
for i in range(len(cities)):
    for j in range(len(cities[i])-1):

        (matrix[ltoi[cities[i][j]]])[ltoi[cities[i][j+1]]]+=1


#Converting into probability
for i in range(27):
    s = matrix[i]
    for j in range(27):
        matrix[i][j] = matrix[i][j]/s
print(matrix)
    
