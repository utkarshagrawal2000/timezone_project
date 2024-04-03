from django.urls import path
from . import views
urlpatterns = [
    path('create_payment_order/', views.create_payment_order.as_view(), name='create_payment_order'),
    

]