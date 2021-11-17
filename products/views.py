from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Min, Avg, Count

from products.models import Product, ProductSize, Category, Brand, Size
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

class ProductListView(View):
    def get(self, request):
        try:
            keyword       = request.GET.get('keyword')
            sorting       = request.GET.get('sort', 'id')
            fast_shipping = request.GET.get('fast_shipping')

            sort = {
                'id'            : 'id',
                'release_date'  : "release_date" ,
                '-release_date' : '-release_date',
                'price'         : 'price',
                '-price'        : '-price'
            }

            q = Q()

            if keyword:
                q = Q(brand__name=keyword) | Q(en_name__icontains=keyword) | Q(ko_name__contains=keyword)

            if fast_shipping:
                q = Q(fast_shipping=fast_shipping)

            products = Product.objects.filter(q).select_related('brand')\
                                                .annotate(price=Min('productsize__bidding__price', filter=Q(productsize__bidding__bid_type_id=2)))\
                                                .order_by(sort[sorting])
            
            result = {
                'productslist': [{
                    'id'           : product.id,
                    'brand'        : product.brand.name,
                    'en_name'      : product.en_name,
                    'ko_name'      : product.ko_name,
                    'buy_now_price': product.price,
                    'image_url'    : product.images.values('url')[0],
                    'fast_shipping': product.fast_shipping
                } for product in products],
                'category'     : [category.name for category in Category.objects.all()],
                'brand'        : [brand.name for brand in Brand.objects.all()],
                'size'         : [size.name for size in Size.objects.all()]
            }
            return JsonResponse({'products': result}, status=200)

        except :         
            return JsonResponse({'message': "Doesnotexist"}, status=404)