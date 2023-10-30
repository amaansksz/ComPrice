from django.urls import path
from Price import views

urlpatterns = [
    path('', views.index, name='home'),  # This sets 'home.html' as the main landing page
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contactus/', views.contactus, name='contactus'),
    path('how/', views.how, name='how'),
    path('Search/', views.Search, name='Search'),
    path('results/', views.results, name='results'),
    path('search/', views.search_product, name='search_product'),
]
