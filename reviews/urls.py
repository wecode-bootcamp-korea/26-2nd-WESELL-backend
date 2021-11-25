from django.urls import path
from reviews.views import ReviewListView, CommentsView

urlpatterns = [
    path('', ReviewListView.as_view()),
    path('/<int:review_id>/comment', CommentsView.as_view())
] 