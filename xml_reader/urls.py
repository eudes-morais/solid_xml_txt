# xml_reader/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Mapeia a URL raiz para a nossa nova view
    path('', views.upload_multiple_xml, name='upload_multiple_xml'),
    path('download/<int:file_index>/', views.download_txt, name='download_txt'),
    path('download-all/', views.download_all_txt, name='download_all_txt'),
    path('resultados/', views.resultados_page, name='resultados'),
]