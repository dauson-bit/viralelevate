from django.contrib import admin
from .models import PaymentSupportRequest, Package , Service, Order

class ServiceInline(admin.TabularInline):
  model= Service
  extra=1

class PackageAdmin(admin.ModelAdmin):
  list_display=('name','id')
  inlines=[ServiceInline]

admin.site.register(PaymentSupportRequest)
admin.site.register(Package, PackageAdmin)
admin.site.register(Service)
admin.site.register(Order)
