from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.views import APIView 

import json

# import findspark
# findspark.init()

import numpy as np
import pandas as pd
import pickle
import sklearn
 

# Load Models 

symbol_encoder = pickle.load(open("app/symbol_target_encoder.sav", 'rb'))
linear_regression_model = pickle.load(open("app/linear_regression.sav", 'rb'))

def index(request): 
  context = {
  }
  return render(request, "main_app/index.html", context)

class PredictAPIView(APIView):

    def get(self,request):
        if request.method == 'GET':
            
            # sentence is the query we want to get the prediction for
            symbol =  request.GET.get('symbol')
            vol_moving_avg = request.GET.get('vol_moving_avg')
            adj_close_rolling_med = request.GET.get('adj_close_rolling_med')

            array_1 = np.array([[symbol,vol_moving_avg,adj_close_rolling_med]])
            # array_1 = np.array([['AB',1000,100]])
            df = pd.DataFrame(array_1, columns=['Symbol', 'vol_moving_avg', 'adj_close_rolling_med'])

            df['Symbol_2'] = symbol_encoder.transform(df['Symbol']) 
            df = df.drop('Symbol', axis = 1) 
            y_pred = linear_regression_model.predict(df)


            # predict method used to get the prediction
            response = {'prediction': y_pred[0]}
            
            # returning JSON response
            return JsonResponse(response)
