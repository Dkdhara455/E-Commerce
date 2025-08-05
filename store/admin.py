from django.contrib import admin
from store.models import *
# Register your models here.
admin.site.register(Product1)
admin.site.register(UserProfile)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)