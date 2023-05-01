from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name= "index"),
    path('predict/',views.PredictAPIView.as_view(),name="predict"),
]
