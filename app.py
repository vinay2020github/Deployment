#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask
from flask import render_template
from flask import request


# In[ ]:


import jsonify
import requests
import pickle


# In[ ]:


import pandas as pd
import numpy as np


# In[ ]:


app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/', methods = ['GET'])

def Home():
    return render_template('index.html')


# In[ ]:


@app.route('/predict', methods = ['POST'])

def predict():
    
    Fuel_Type_Diesel = 0
    
    if request.methods == 'POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        
        if(Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif(Fuel_Type_Petrol == 'Diesel'):
            Fuel_Type_Diesel = 1
            Fuel_Type_Petrol = 0
        else:
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol = 0
            
        Year = 2021 - Year
        
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if(Seller_Type_Individual == 'Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        
        Transmission_Manual = request.form['Transmission_Manual']
        if(Transmission_Manual == 'Manual'):
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0
            
        prediction = model.predict([['Present_Price',
                                     'Kms_Driven','Owner','car_age',
                                     'Fuel_Type_Diesel', 'Fuel_Type_Petrol',
                                     'Seller_Type_Individual', 'Transmission_Manual']])
        
        output = round(prediction[0], 2)
        
        if output < 0:
            return render_template('index.html', prediction_texts = "Sorry, you can not sell this car {}".format(output))
        else:
            return render_template('index.html', prediction_texts = "Sorry, you can sell this car at price =  {}".format(output))
    
    else:
        return reder_template('index.html')
    


# In[ ]:


if __name__ == '__main__':
    app.run(debug = False)

