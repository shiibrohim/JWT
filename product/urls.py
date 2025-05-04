from django.urls import path
from .views import CreateAPIView, ProductListAPIView, DetailAPIView, UpdateAPIView, DeleteAPIView

urlpatterns = [
    path('create/', CreateAPIView.as_view(), name='create'),
    path('product/', ProductListAPIView.as_view(), name='list'),
    path('product/<int:pk>/', DetailAPIView.as_view(), name='detail'),
    path('product/<int:pk>/update/', UpdateAPIView.as_view(), name='update'),
    path('product/<int:pk>/delete/', DeleteAPIView.as_view(), name='delete'),
]