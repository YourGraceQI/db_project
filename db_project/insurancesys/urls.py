
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customer', views.customer, name='customer'),
    path('policy', views.policy, name='policy'),
    path('invoice', views.invoice, name='invoice'),
    path('payment', views.payment, name='payment'),
    path('vehicle', views.vehicle, name='vehicle'),
    path('driver', views.driver, name='driver'),
    path('home', views.home, name='home'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
]