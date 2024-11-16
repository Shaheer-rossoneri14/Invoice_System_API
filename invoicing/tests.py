from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer

class ItemModelTestCase(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name="Test Item",
            price=10.99,
            description="A test item description",
            stock=100
        )

    def test_item_creation(self):
        """Test that the Item model creates an item correctly"""
        self.assertEqual(self.item.name, "Test Item")
        self.assertEqual(self.item.price, 10.99)
        self.assertEqual(self.item.description, "A test item description")
        self.assertEqual(self.item.stock, 100)

    def test_item_string_representation(self):
        """Test the string representation of an item"""
        self.assertEqual(str(self.item), "Test Item")


class ItemSerializerTestCase(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name="Test Item",
            price=10.99,
            description="A test item description",
            stock=100
        )
        self.serializer = ItemSerializer(instance=self.item)

    def test_item_serialization(self):
        """Test that the serializer correctly serializes item data"""
        data = self.serializer.data
        self.assertEqual(data['name'], self.item.name)
        self.assertEqual(data['price'], str(self.item.price))  # Decimal fields are serialized as strings
        self.assertEqual(data['description'], self.item.description)
        self.assertEqual(data['stock'], self.item.stock)

    def test_item_deserialization(self):
        """Test that the serializer correctly deserializes valid data"""
        data = {
            "name": "New Item",
            "price": "20.50",
            "description": "A new item description",
            "stock": 50
        }
        serializer = ItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        item = serializer.save()
        self.assertEqual(item.name, "New Item")
        self.assertEqual(item.price, 20.50)
        self.assertEqual(item.description, "A new item description")
        self.assertEqual(item.stock, 50)

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
            price=15.50,
            description="Second test item",
            stock=30
        )

    def test_get_items_list(self):
        """Test that the API returns the correct list of items"""
        response = self.client.get('/api/items/')  # Replace with the correct endpoint if different
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_empty_items_list(self):
        """Test that the API returns an empty list if no items exist"""
        Item.objects.all().delete()
        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
