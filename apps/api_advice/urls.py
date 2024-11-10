from django.urls import path
from .views import conselho  

urlpatterns = [
    path("conselho/", conselho, name='conselho'),
]
