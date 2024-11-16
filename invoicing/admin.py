from django.contrib import admin
from .models import Item, Purchase, PurchaseItem

# Admin interface configuration for the Item model
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'description')
    
    # Enable search functionality by item name
    search_fields = ('name',)

# Admin interface configuration for the Purchase model
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    
    # Add a filter for the 'created_at' field in the list view
    list_filter = ('created_at',)

# Admin interface configuration for the PurchaseItem model
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'item', 'quantity')
    
    # Enable search functionality by item name within PurchaseItem
    search_fields = ('item__name',)

admin.site.register(Item, ItemAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseItem, PurchaseItemAdmin)
