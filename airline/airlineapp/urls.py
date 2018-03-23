from django.urls import path, include
from . import views



app_name = 'airlineapp'
urlpatterns = [
    path('api/findflight/', views.findflight),
    path('api/bookflight/', views.bookflight),
    path('api/paymentmethods/', views.paymentmethods),
    path('api/payforbooking/', views.payforbooking),

    path('api/finalizebooking/', views.finalizebooking),
    path('api/bookingstatus/', views.bookingstatus),
    path('api/cancelbooking/', views.cancelbooking),
]
