from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tree_data/', views.tree_data, name='tree_data'),
]