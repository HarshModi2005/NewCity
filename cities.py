# Imports
import numpy as np
import pandas as pd
import string
import random
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

#Reading the data
data = pd.read_csv('NewCity/india.csv')
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
matrix = np.zeros((27, 27,27))

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

#First letter - row second letter - column third letter height
for i in range(len(cities)):
    for j in range(len(cities[i])-1-1):
        
           ((matrix[ltoi[cities[i][j]]])[ltoi[cities[i][j+1]]])[ltoi[cities[i][j+2]]]+=1


#Converting into probability
for i in range(27):
    for j in range(27):
        s= sum(matrix[i][j])
        for k in range(27):
    
            if s != 0:  # Check that s is not zero
                matrix[i][j][k] = matrix[i][j][k]/s
            
#AB bari aati h neural network ki

# # # # Preparing the xTrain and yTrain
xTrain =[]
for i in range(27):
    for j in range(27):
        # xTrain.append(int(str(i)+ str(j)))
        xTrain.append([i,j])
print(xTrain)
#yTrain is maximum of each list 
yTrain=[]
for i in range(27):
    for j in range(27):
        yTrain.append(ltoi[itol[list(matrix[i][j]).index(max(matrix[i][j]))]])


# Convert lists to numpy arrays
xTrain = np.array(xTrain)
yTrain = np.array(yTrain)


# Define the model
model = Sequential([
    Dense(256, activation='relu', ),
    Dense(64, activation='relu'),
    Dense(27, activation='softmax'),  
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'],
)


# # Load the model from the file
# model = load_model('my_model.h5')
#Train the model
# model.fit(xTrain, yTrain, epochs=65000)

# model.save('india_city.h5')
model = load_model('india_city.h5')
#Predicting 
#Set for intializing string
table={}
for i in letters:
    table[i] =0

for i in cities:
    table[i[1]]+=1
key = table.keys()
val = list(table.values())
val = [x/sum(val) for x in val]
val = np.array(val).reshape(1,-1)

generated_cities = []

for i in range(20):
    s=  tf.random.categorical(val, 1)[0][0]
    s= '.' + itol[s.numpy()]
    
    while s[-1] != "." :
        # input_data = np.array([[int(str(ltoi[s[-2]])+ str(ltoi[s[-1]]))]])
        input_data = [[ltoi[s[-2]],ltoi[s[-1]]]]
        prediction = model.predict(input_data)
        
        s+= itol[list(prediction[0]).index(max(prediction[0]))]
        if s[-1] == "." and len(s)<10:
            s = s[0:len(s)-1]
            s+= itol[(tf.random.categorical(val, 1)[0][0]).numpy()]
    
    generated_cities.append(s)   

print(generated_cities)


# c=0
# for i in cities:
#     if 'ang' in i:
#         c+=1
# print(c)
# print(len(cities))
