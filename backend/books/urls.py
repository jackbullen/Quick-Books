from django.urls import path
from .views import BookList, BookDetail, ReviewList #BookReviewList

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<slug:slug>/', BookDetail.as_view(), name='book-detail'),
    # path('books/<slug:slug>/reviews/', BookReviewList.as_view(), name='book-review-list'),
    path('books/<slug:slug>/reviews', ReviewList.as_view(), name='write-review'),
]
