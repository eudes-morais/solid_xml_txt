# xml_reader/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Mapeia a URL raiz para a nossa nova view
    path('', views.upload_multiple_xml, name='upload_multiple_xml'),
]