from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Item, Purchase, PurchaseItem
from .serializers import ItemSerializer, PurchaseItemSerializer, PurchaseSerializer
from io import BytesIO
from PyPDF2 import PdfReader
from django.urls import reverse

class ItemModelTestCase(TestCase):
    def setUp(self):
        """Set up an item instance for testing."""
        self.item = Item.objects.create(
            name="Test Item",
            price=15.99,
            description="A test item description",
            stock=100
        )

    def test_item_creation(self):
        """Test that an item is created successfully."""
        self.assertEqual(self.item.name, "Test Item")
        self.assertEqual(self.item.price, 15.99)
        self.assertEqual(self.item.description, "A test item description")
        self.assertEqual(self.item.stock, 100)

    def test_string_representation(self):
        """Test the string representation of the item."""
        self.assertEqual(str(self.item), "Test Item")

    def test_stock_default(self):
        """Test that the stock field defaults to 0 if not provided."""
        item_no_stock = Item.objects.create(
            name="No Stock Item",
            price=5.00,
            description="An item without stock"
        )
        self.assertEqual(item_no_stock.stock, 0)

class PurchaseModelTestCase(TestCase):
    def setUp(self):
        """Set up purchases and items for testing."""
        self.item1 = Item.objects.create(
            name="Item 1",
            price=10.00,
            description="First item",
            stock=50
        )
        self.item2 = Item.objects.create(
            name="Item 2",
            price=20.00,
            description="Second item",
            stock=30
        )
        self.purchase = Purchase.objects.create()

    def test_purchase_creation(self):
        """Test that a purchase is created successfully."""
        self.assertIsNotNone(self.purchase.created_at)

    def test_items_in_purchase(self):
        """Test adding items to a purchase via PurchaseItem."""
        PurchaseItem.objects.create(purchase=self.purchase, item=self.item1, quantity=2)
        PurchaseItem.objects.create(purchase=self.purchase, item=self.item2, quantity=3)

        # Verify that the items are linked to the purchase
        self.assertEqual(self.purchase.items.count(), 2)
        self.assertIn(self.item1, self.purchase.items.all())
        self.assertIn(self.item2, self.purchase.items.all())

class PurchaseItemModelTestCase(TestCase):
    def setUp(self):
        """Set up items and purchase for PurchaseItem tests."""
        self.item = Item.objects.create(
            name="Test Item",
            price=12.99,
            description="A test item",
            stock=10
        )
        self.purchase = Purchase.objects.create()
        self.purchase_item = PurchaseItem.objects.create(
            purchase=self.purchase,
            item=self.item,
            quantity=5
        )

    def test_purchase_item_creation(self):
        """Test that a PurchaseItem is created successfully."""
        self.assertEqual(self.purchase_item.purchase, self.purchase)
        self.assertEqual(self.purchase_item.item, self.item)
        self.assertEqual(self.purchase_item.quantity, 5)

    def test_quantity_is_positive(self):
        """Test that the quantity is positive."""
        with self.assertRaises(ValueError):
            PurchaseItem.objects.create(
                purchase=self.purchase,
                item=self.item,
                quantity=-3
            )

class ItemSerializerTestCase(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name="Test Item",
            price=15.99,
            description="A test item description",
            stock=100
        )

    def test_item_serialization(self):
        """Test that the serializer correctly serializes item data."""
        serializer = ItemSerializer(self.item)
        data = serializer.data
        self.assertEqual(data['name'], self.item.name)
        self.assertEqual(data['price'], str(self.item.price))  # Decimal is serialized as string
        self.assertEqual(data['description'], self.item.description)
        self.assertEqual(data['stock'], self.item.stock)

    def test_item_deserialization(self):
        """Test that the serializer correctly deserializes valid data."""
        data = {
            "name": "New Item",
            "price": "20.50",
            "description": "A new test item description",
            "stock": 50
        }
        serializer = ItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        item = serializer.save()
        self.assertEqual(item.name, "New Item")
        self.assertEqual(item.price, 20.50)
        self.assertEqual(item.description, "A new test item description")
        self.assertEqual(item.stock, 50)

class PurchaseItemSerializerTestCase(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name="Test Item",
            price=15.99,
            description="A test item description",
            stock=100
        )
        self.purchase = Purchase.objects.create()
        self.purchase_item = PurchaseItem.objects.create(
            purchase=self.purchase,
            item=self.item,
            quantity=2
        )

    def test_purchase_item_serialization(self):
        """Test that the serializer correctly serializes purchase item data."""
        serializer = PurchaseItemSerializer(self.purchase_item)
        data = serializer.data
        self.assertEqual(data['item'], self.item.id)
        self.assertEqual(data['quantity'], self.purchase_item.quantity)

    def test_purchase_item_deserialization(self):
        """Test that the serializer correctly deserializes valid data."""
        data = {
            "item": self.item.id,
            "quantity": 5
        }
        serializer = PurchaseItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        purchase_item = serializer.save(purchase=self.purchase)
        self.assertEqual(purchase_item.item, self.item)
        self.assertEqual(purchase_item.quantity, 5)

class PurchaseSerializerTestCase(TestCase):
    def setUp(self):
        self.item1 = Item.objects.create(
            name="Item 1",
            price=10.00,
            description="First test item",
            stock=50
        )
        self.item2 = Item.objects.create(
            name="Item 2",
            price=20.00,
            description="Second test item",
            stock=30
        )
        self.purchase = Purchase.objects.create()
        self.purchase_item1 = PurchaseItem.objects.create(
            purchase=self.purchase,
            item=self.item1,
            quantity=2
        )
        self.purchase_item2 = PurchaseItem.objects.create(
            purchase=self.purchase,
            item=self.item2,
            quantity=3
        )

    def test_purchase_serialization(self):
        """Test that the serializer correctly serializes purchase data."""
        serializer = PurchaseSerializer(self.purchase)
        data = serializer.data
        self.assertEqual(len(data['items']), 2)
        self.assertEqual(data['items'][0]['item'], self.item1.id)
        self.assertEqual(data['items'][0]['quantity'], 2)
        self.assertEqual(data['items'][1]['item'], self.item2.id)
        self.assertEqual(data['items'][1]['quantity'], 3)

    def test_purchase_deserialization(self):
        """Test that the serializer correctly deserializes purchase data."""
        data = {
            "items": [
                {"item": self.item1.id, "quantity": 2},
                {"item": self.item2.id, "quantity": 3}
            ]
        }
        serializer = PurchaseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        purchase = serializer.save()
        self.assertEqual(purchase.items.count(), 2)
        purchase_items = purchase.purchaseitem_set.all()
        self.assertEqual(purchase_items[0].item, self.item1)
        self.assertEqual(purchase_items[0].quantity, 2)
        self.assertEqual(purchase_items[1].item, self.item2)
        self.assertEqual(purchase_items[1].quantity, 3)

class ItemListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item1 = Item.objects.create(
            name="Item 1",
            price=10.00,
            description="First test item",
            stock=50
        )
        self.item2 = Item.objects.create(
            name="Item 2",
            price=20.00,
            description="Second test item",
            stock=30
        )

    def test_get_items_list(self):
        """Test that the API returns the correct list of items."""
        response = self.client.get('/api/items/')  # Replace with the actual endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.item1.name)
        self.assertEqual(response.data[1]['name'], self.item2.name)

class CreatePurchaseViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test items
        self.item1 = Item.objects.create(
            name="Item 1",
            price=10.00,
            description="First test item",
            stock=50
        )
        self.item2 = Item.objects.create(
            name="Item 2",
            price=20.00,
            description="Second test item",
            stock=30
        )

        # Define valid and invalid data
        self.valid_data = {
            "items": [
                {"id": self.item1.id, "quantity": 5},
                {"id": self.item2.id, "quantity": 10}
            ]
        }
        self.invalid_data = {
            "items": [
                {"id": self.item1.id, "quantity": 60}  # Exceeds available stock
            ]
        }

        # Use reverse to dynamically generate the endpoint URL
        self.create_purchase_url = reverse('create-purchase')

    def test_create_purchase_success(self):
        """Test creating a purchase with valid data."""
        response = self.client.post(self.create_purchase_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that one purchase was created
        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.first()

        # Verify the correct number of purchase items
        purchase_items = PurchaseItem.objects.filter(purchase=purchase)
        self.assertEqual(purchase_items.count(), 2)

        # Verify stock updates
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.stock, 45)  # Stock reduced by quantity

    def test_create_purchase_insufficient_stock(self):
        """Test creating a purchase with insufficient stock."""
        response = self.client.post(self.create_purchase_url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify the error message
        self.assertEqual(response.data['error'], f"Not enough stock for {self.item1.name}")

        # Verify stock remains unchanged
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.stock, 50)  # Stock remains unchanged

class UpdatePurchaseViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item1 = Item.objects.create(
            name="Item 1",
            price=10.00,
            description="First test item",
            stock=50
        )
        self.item2 = Item.objects.create(
            name="Item 2",
            price=20.00,
            description="Second test item",
            stock=30
        )
        self.purchase = Purchase.objects.create()
        PurchaseItem.objects.create(purchase=self.purchase, item=self.item1, quantity=5)
        self.update_data = {
            "items": [
                {"id": self.item2.id, "quantity": 15}
            ]
        }
        # Use reverse to dynamically generate the endpoint URL
        self.update_purchase_url = reverse('update-purchase', kwargs={'id': self.purchase.id})

    def test_update_purchase(self):
        """Test updating an existing purchase."""
        response = self.client.put(self.update_purchase_url, self.update_data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Purchase updated successfully")
        self.assertEqual(self.purchase.items.count(), 1)
        self.assertIn(self.item2, self.purchase.items.all())

class InvoiceViewTest(TestCase):
    def setUp(self):
        """
        Set up test data for the InvoiceView.
        """
        self.client = APIClient()

        # Create items
        self.item1 = Item.objects.create(name="Item 1", price=10.00, description="Test Item 1", stock=100)
        self.item2 = Item.objects.create(name="Item 2", price=20.00, description="Test Item 2", stock=100)

        # Create purchase and purchase items
        self.purchase = Purchase.objects.create()
        PurchaseItem.objects.create(purchase=self.purchase, item=self.item1, quantity=2)
        PurchaseItem.objects.create(purchase=self.purchase, item=self.item2, quantity=3)

        # URL for the invoice view
        self.invoice_url = reverse('generate-invoice', kwargs={'id': self.purchase.id})

    def test_generate_invoice_pdf(self):
        """
        Test the generation of a PDF invoice for a given purchase.
        """
        # Send GET request to generate invoice
        response = self.client.get(self.invoice_url)

        # Check if the response returns a PDF file
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.has_header('Content-Disposition'))
        self.assertIn('attachment; filename="invoice.pdf"', response['Content-Disposition'])

        # Validate PDF content
        # Since FileResponse is streamed, we need to join the streaming content
        pdf_stream = b"".join(response.streaming_content)
        pdf_buffer = BytesIO(pdf_stream)
        
        # Use PyPDF2 to read the PDF content
        pdf_reader = PdfReader(pdf_buffer)
        
        # Extract text from all pages
        pdf_text = ''.join([page.extract_text() for page in pdf_reader.pages])

        # Check if the text includes invoice details
        self.assertIn("Invoice", pdf_text)
        self.assertIn("Item 1 x 2 @ 10.0", pdf_text)
        self.assertIn("Item 2 x 3 @ 20.0", pdf_text)
        self.assertIn("Total: 80.0", pdf_text)