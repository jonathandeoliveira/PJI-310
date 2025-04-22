from django.urls import path
from apps.dashboard.views import dashboard_view

urlpatterns = [
    path("dashboard/", dashboard_view, name='dashboard'),
]
