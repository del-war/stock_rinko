from django.contrib import admin
from django.urls import path
from stockmgmt import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('home/', views.home, name='home'),
    path('list_items/', views.list_items, name='list_items'),
    path('add_items/', views.add_items, name='add_items'),
    path('update_items/<str:pk>/', views.update_items, name='update_items'),
    path('delete_items/<str:pk>/', views.delete_items, name='delete_items'),
    path('stock_detail/<str:pk>/', views.stock_detail, name='stock_detail'),
    path('export_items/<str:pk>/', views.export_items, name='export_items'),
    path('import_items/<str:pk>/', views.import_items, name='import_items'),
    path('reorder_level/<str:pk>/', views.reorder_level, name='reorder_level'),
    path('list_history', views.list_history, name='list_history'),
    path('settings/', views.settings, name='settings'),

]
