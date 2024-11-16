from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    # Link items with purchases via a through model (PurchaseItem)
    items = models.ManyToManyField(Item, through='PurchaseItem')
    created_at = models.DateTimeField(auto_now_add=True) 

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
