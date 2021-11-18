import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Min, Avg, Count

from products.models import Product, ProductSize
from biddings.models import BidType, Order

class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'message' : 'DOES NOT EXISTS'}, status=404)
        
        product   = Product.objects.get(id=product_id)
        dates     = [data for data in Order.objects.filter(productsize__product=product, status='거래완료').values('created_at').annotate(count=Count('id'))]
        bid_types = [data for data in BidType.objects.filter(bidding__productsize__product=product).values('name').annotate(count=Count('id'))]
        
        result = {
            'product_info'  : {
                'id'            : product.id,
                'brand'         : product.brand.name,
                'en_name'       : product.en_name,
                'ko_name'       : product.ko_name,
                'model_number'  : product.model_number,
                'release_date'  : product.release_date,
                'color'         : product.color,
                'release_price' : product.release_price,
                'fast_shipping' : product.fast_shipping
            },
            'product_image' : [{
                'id'  : product_image.id,
                'url' : product_image.url,
            } for product_image in product.images.all()],
            'lowest_price_by_size' : [{
                    'bid_type' : bid_type['name'],
                    'sizes'    : [{
                        'id'           : product_size.id,
                        'size'         : product_size.size.name,
                        'lowest_price' : product_size.lowest_price
                    } for product_size in ProductSize.objects.filter(product=product, bidding__bid_type__name=bid_type['name'])\
                                                             .annotate(lowest_price=Min('bidding__price'))\
                                                             .select_related('size')]
            } for bid_type in bid_types],
            'market_price'   : [{
                'date'  : date['created_at'],
                'sizes' : [{
                    'size'      : product_size.size.name,
                    'avg_price' : product_size.avg_price
                } for product_size in ProductSize.objects.filter(order__created_at=date['created_at'], product=product)\
                                                         .annotate(avg_price=Avg('order__price'))\
                                                         .select_related('size')]
            } for date in dates],
            'order_history'     : [{
                'id'         : order.id,
                'size'       : order.productsize.size.name,
                'price'      : order.price,
                'created_at' : order.created_at
            } for order in Order.objects.filter(productsize__product=product).select_related('productsize__size').order_by('-created_at')]
        }
        
        return JsonResponse({'result' : result}, status = 200)