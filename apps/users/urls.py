from django.urls import path
from apps.users import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_professor/', views.register_professor, name='register_professor'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
