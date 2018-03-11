from django.urls import path, include
from . import views



app_name = 'airlineapp'
urlpatterns = [
    path('findflight/', views.findflight),
    path('bookflight/', views.bookflight),
    path('paymentmethods/', views.paymentmethods),
    path('payforbooking/', views.payforbooking),

    path('finalizebooking/', views.finalizebooking),
    path('bookingstatus/', views.bookingstatus),
    path('cancelbooking/', views.cancelbooking),
]
