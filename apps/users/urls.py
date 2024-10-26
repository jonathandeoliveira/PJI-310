from django.urls import path
from apps.users import views
from .views import CustomLoginView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
