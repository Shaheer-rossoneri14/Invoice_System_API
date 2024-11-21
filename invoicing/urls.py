from django.urls import path
from .views import CreatePurchaseView, ItemListView, UpdatePurchaseView, InvoiceView

urlpatterns = [
    path('items/', ItemListView.as_view(), name='item-list'),
    path('purchase/', CreatePurchaseView.as_view(), name='create-purchase'),
    path('purchase/<int:id>/', UpdatePurchaseView.as_view(), name='update-purchase'),
    path('invoice/<int:id>/', InvoiceView.as_view(), name='generate-invoice'),
]
