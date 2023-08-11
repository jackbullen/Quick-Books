from rest_framework import generics
from .models import Book, Review
from django.shortcuts import render
from .serializer import BookSerializer, ReviewSerializer

class BookList(generics.ListCreateAPIView):    
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    
    def get_object(self):
        book = Book.objects.get(slug=self.kwargs['slug'])
        return book

class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            book = Book.objects.get(slug=slug)
            return Review.objects.filter(book=book)
        
        except Book.DoesNotExist:
            return Review.objects.none()
    