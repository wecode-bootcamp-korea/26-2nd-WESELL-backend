from django.urls import path
from .views import *

urlpatterns = [
    path('/<int:product_id>', BiddingListView.as_view()),
    path('/<int:product_id>/orders', OrderListView.as_view())
] 