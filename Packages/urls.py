from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('one-time-growth/', views.one_time_growth, name='one_time_growth'),
    path('api/package/<int:package_id>/services/', views.get_package_services, name='get_package_services'),
    path('submit-order/', views.submit_order, name='submit_order'),
    path('payment-guide/<int:order_id>/', views.payment_guide, name='payment_guide'),
    path('payment-gateway/<int:order_id>/', views.payment_gateway, name='payment_gateway'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 