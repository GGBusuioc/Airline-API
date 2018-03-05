from django.urls import path, include
from . import views



app_name = 'airlineapp'
urlpatterns = [
    path('findflight/', views.findflight),
    path('bookflight/', views.bookflight),

]
