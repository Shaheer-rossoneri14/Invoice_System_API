from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item, Purchase, PurchaseItem
from .serializers import ItemSerializer

class ItemListView(APIView):
    # Fetch and return all items
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
class CreatePurchaseView(APIView):
    # Create a new purchase
    def post(self, request):
        data = request.data
        
        purchase = Purchase.objects.create()
        
        for item_data in data['items']:
            item = Item.objects.get(id=item_data['id'])
            
            # Check if enough stock is available
            if item.stock >= item_data['quantity']:
                item.stock -= item_data['quantity']
                item.save()
                PurchaseItem.objects.create(
                    purchase=purchase,
                    item=item,
                    quantity=item_data['quantity']
                )
            else:
                return Response({"error": f"Not enough stock for {item.name}"}, status=400)
        
        return Response({"purchase_id": purchase.id}, status=201)
    
class UpdatePurchaseView(APIView):
    # Update an existing purchase
    def put(self, request, id):
        purchase = Purchase.objects.get(id=id)
        purchase.items.clear()
        
        for item_data in request.data['items']:
            item = Item.objects.get(id=item_data['id'])
            PurchaseItem.objects.create(
                purchase=purchase,
                item=item,
                quantity=item_data['quantity']
            )
        
        return Response({"message": "Purchase updated successfully"})
