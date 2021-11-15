from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'categories'

class Brand(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'brands'

class Product(models.Model):
    en_name       = models.CharField(max_length=100)
    ko_name       = models.CharField(max_length=100)
    model_number  = models.CharField(max_length=40)
    color         = models.CharField(max_length=40)
    release_date  = models.DateField()
    release_price = models.PositiveIntegerField()
    category      = models.ForeignKey('Category',on_delete=models.CASCADE)
    brand         = models.ForeignKey('Brand',on_delete=models.CASCADE)
    size          = models.ManyToManyField('Size', through='ProductSize')
    
    class Meta:
        db_table = 'products'

class Size(models.Model):
    name = models.CharField(max_length=40)
    
    class Meta:
        db_table = 'sizes'

class ProductSize(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size    = models.ForeignKey('Size', on_delete=models.CASCADE)
   
    class Meta:
        db_table = 'products_sizes'

class ProductImage(models.Model):
    url     = models.CharField(max_length=2000)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'product_images'