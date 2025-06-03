from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('social_media/', views.social_media, name='social_media'),
    path('submit-support/', views.submit_payment_support, name='submit_payment_support'),
    path('one-time-growth/', views.one_time_growth, name='one_time_growth'),
    path('api/package/<int:package_id>/services/', views.get_package_services, name='get_package_services'),
    path('submit-order/', views.submit_order, name='submit_order'),
    path('payment-guide/<int:order_id>/', views.payment_guide, name='payment_guide'),
    path('payment-gateway/<int:order_id>/', views.payment_gateway, name='payment_gateway'),
    path('initiate-payment/<int:order_id>/', views.initiate_payment, name='initiate_payment'),
    path('mpesa/callback/<int:order_id>/', views.mpesa_callback, name='mpesa_callback'),
    path('check-payment-status/<int:order_id>/', views.check_payment_status, name='check_payment_status'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 