from django.urls import path
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('request_service/', views.request_service, name='request_service'),
    path('create_post/',views.create_post, name='create_post'),
    path('purchase/',views.purchase, name='purchase'),
    path('shop_store/',views.shop_store, name='shop_store'),
    path('about', views.about_us, name='about'),
]
