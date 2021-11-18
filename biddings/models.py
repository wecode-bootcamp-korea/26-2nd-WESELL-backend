from django.db import models

class Bidding(models.Model):
    user        = models.ForeignKey('users.User',on_delete=models.CASCADE)
    productsize = models.ForeignKey('products.ProductSize',on_delete=models.CASCADE)
    bid_type    = models.ForeignKey('BidType',on_delete=models.CASCADE)
    price       = models.PositiveIntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'biddings'

class BidType(models.Model):
    name = models.CharField(max_length=40)
    
    class Meta:
        db_table = 'bid_types'

class Order(models.Model):
    buyer       = models.ForeignKey('users.User',on_delete=models.CASCADE, related_name='buyer')
    seller      = models.ForeignKey('users.User',on_delete=models.CASCADE, related_name='seller')
    status      = models.CharField(max_length=40)
    productsize = models.ForeignKey('products.ProductSize',on_delete=models.CASCADE)
    price       = models.PositiveIntegerField()
    created_at  = models.DateField(auto_now_add=True)
    updated_at  = models.DateField(auto_now=True)

    class Meta:
        db_table = 'orders'