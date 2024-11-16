from rest_framework import serializers
from .models import Item, Purchase, PurchaseItem

# Serializer to convert Item model into JSON format (or vice versa).
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'description', 'stock']
        
# Serializer to handle the linking of items to a purchase with quantity.
# This serializer is used to serialize each item within a purchase, along with the quantity.
class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = ['item', 'quantity']
        
class PurchaseSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    # Custom field to represent the associated items in a purchase.
    # By default, the 'items' field would serialize the related PurchaseItems using the PurchaseItemSerializer, 
    # but we're overriding it to return a custom structure.

    class Meta:
        model = Purchase
        fields = ['id', 'items', 'created_at']
        # Serialize the Purchase model, including its ID, associated items, and creation date.

    def get_items(self, obj):
        # Custom representation for read operations (GET requests)
        purchase_items = PurchaseItem.objects.filter(purchase=obj)  # Fetch all PurchaseItem objects related to the purchase
        return [
            {"item": purchase_item.item.id, "quantity": purchase_item.quantity}
            for purchase_item in purchase_items
        ]
        # Here we return the IDs of the items in the purchase, along with their quantities. 
        # The 'items' field in the response will contain a list of dictionaries with 'item' (ID) and 'quantity'.

    def create(self, validated_data):
        # Handle nested creation for write operations (POST requests)
        # We access the raw input data (self.initial_data) to process the items.
        items_data = self.initial_data['items']  # Access the raw input data for 'items'

        # Create the purchase instance
        purchase = Purchase.objects.create()

        for item_data in items_data:
            # For each item in the items data, retrieve the item object and create a PurchaseItem
            item = Item.objects.get(id=item_data['item'])  # Fetch the Item object using its ID
            PurchaseItem.objects.create(
                purchase=purchase,  # Link the PurchaseItem to the newly created purchase
                item=item,  # Link the PurchaseItem to the Item
                quantity=item_data['quantity']  # Set the quantity of the item in the purchase
            )
        
        return purchase
        # The method returns the created Purchase instance with all associated PurchaseItems.
        # This will be automatically serialized and returned in the API response.
