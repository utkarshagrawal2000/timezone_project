from django.urls import path
from . import views
urlpatterns = [
    path('create_payment_order/', views.create_payment_order, name='create_payment_order'),
    

]