from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_tree', views.add_tree, name='add_tree'),
    path('logout/', views.logout, name='logout'),
    path('tree/<int:tree_id>/', views.tree_details, name='tree_details'),
    path('tree/<int:tree_id>/edit/', views.edit_tree, name='edit_tree'),
    path('tree/<int:tree_id>/delete/', views.delete_tree, name='delete_tree'),
    path('visit_tree/<int:tree_id>/', views.visit_tree, name='visit_tree'),
    path('register', views.index, name='register'),
    path('login', views.index, name='login'),
    path('zip_code/<str:zip_code>/',
         views.zip_code, name='zip_code'),
]
