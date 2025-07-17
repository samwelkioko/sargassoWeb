from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('About-Us', views.about, name='about'),
    path('Our-Service', views.offer, name='service'),
    path('Our-impact', views.impact_view, name='impact'),
    path('Supply-Us', views.droppoint, name='supply_us'),
    path('Our-Products', views.product, name='our_products'),
    path('chart-data/', views.chart_data_by_year, name='chart_data_by_year'),
    path('admin/upload', views.import_excel, name='import_excel'),
    
  


    
]