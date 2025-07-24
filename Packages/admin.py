from django.contrib import admin
from .models import  Package , Service, Order

class ServiceInline(admin.TabularInline):
  model= Service
  extra=1

class PackageAdmin(admin.ModelAdmin):
  list_display=('name','id')
  inlines=[ServiceInline]

#class OrderAdmin(admin.ModelAdmin):
  #list_display=('customer_name', 'customer_phone','transaction_id')

admin.site.register(Package, PackageAdmin)
admin.site.register(Service)
admin.site.register(Order)


