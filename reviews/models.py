from django.db import models

class Review(models.Model):
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product    = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    content    = models.CharField(max_length=2000)
    image_url  = models.CharField(max_length=2000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'

class Comment(models.Model):
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    review     = models.ForeignKey('Review', on_delete=models.CASCADE)
    content    = models.CharField(max_length=2000)
    image_url  = models.CharField(max_length=2000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'