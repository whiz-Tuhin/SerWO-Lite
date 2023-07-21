from django.urls import path
from app.views import execute

urlpatterns = [
    path('api/v1/xfaaslite/execute', execute, name='execute'),
]