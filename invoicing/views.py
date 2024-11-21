from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item, Purchase, PurchaseItem
from .serializers import ItemSerializer


from django.http import FileResponse
from reportlab.pdfgen import canvas
from io import BytesIO

class ItemListView(APIView):
    """
    API View to fetch and return a list of all available items.
    """

    def get(self, request):
        """
        Handle GET requests to retrieve all items.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A JSON response containing a list of items with details
            like name, price, description, and stock.
        """
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)


class CreatePurchaseView(APIView):
    """
    API View to handle the creation of a new purchase.
    """

    def post(self, request):
        """
        Handle POST requests to create a new purchase.

        Args:
            request: The HTTP request object containing a list of items to purchase.

        Returns:
            Response: A JSON response containing the purchase ID if successful,
            or an error message if the stock is insufficient.

        Payload format:
        {
            "items": [
                {
                    "id": 1,
                    "quantity": 2
                },
                {
                    "id": 3,
                    "quantity": 1
                }
            ]
        }
        """
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
    """
    API View to handle updating an existing purchase.
    """

    def put(self, request, id):
        """
        Handle PUT requests to update the list of items in a purchase.

        Args:
            request: The HTTP request object containing the updated list of items.
            id: The ID of the purchase to update.

        Returns:
            Response: A JSON response indicating the update status.

        Payload format:
        {
            "items": [
                {
                    "id": 1,
                    "quantity": 5
                },
                {
                    "id": 2,
                    "quantity": 3
                }
            ]
        }
        """
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

class InvoiceView(APIView):
    def get(self, request, id):
        """
        Generate a PDF invoice for a given purchase.

        Args:
            request: The HTTP request object.
            id: The ID of the purchase to generate the invoice for.

        Returns:
            FileResponse: A response containing the generated PDF file as an attachment.
        """
        # Retrieve the purchase object by ID
        purchase = Purchase.objects.get(id=id)

        # Create an in-memory buffer to hold the PDF data
        buffer = BytesIO()

        # Initialize a PDF canvas
        pdf = canvas.Canvas(buffer)

        # Add invoice title
        pdf.drawString(100, 800, "Invoice")

        # Start adding purchase item details at the specified position
        y = 750
        for item in purchase.purchaseitem_set.all():
            # Write item name, quantity, and price
            pdf.drawString(100, y, f"{item.item.name} x {item.quantity} @ {item.item.price}")
            y -= 20

        # Calculate and display the total price
        total = sum([p.item.price * p.quantity for p in purchase.purchaseitem_set.all()])
        pdf.drawString(100, y - 20, f"Total: {total}")

        # Finalize the PDF content and save it
        pdf.showPage()
        pdf.save()

        # Rewind the buffer to the beginning
        buffer.seek(0)

        # Return the generated PDF file as a downloadable response
        return FileResponse(buffer, as_attachment=True, filename='invoice.pdf')