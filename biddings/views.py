import json, re

from django.http      import JsonResponse
from django.views     import View
from json.decoder     import JSONDecodeError

from .models          import *
from products.models  import *
from core.utils       import *
from enum             import Enum

class BidType(Enum):
    BUYING  = 1,
    SELLING = 2,

class BiddingListView(View):
    @login_decorator
    def post(self, request, product_id):
        data = json.loads(request.body)
        try:
            if not re.match('^(0|[1-9]+[0-9]*)$',str(data['price'])):
                return JsonResponse({"message": "올바른 가격 정보를 입력해 주세요."})            
            
            Bidding.objects.create(
                user_id        = request.user.id,
                productsize_id = ProductSize.objects.get(product=product_id, size__name=data['productsize']).id,
                bid_type_id    = data['bid_type'],
                price          = data['price'],
            )
            
            return JsonResponse({'message': "SUCCESS"}, status=201)
        
        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
    
    @login_decorator
    def delete(self, request, product_id):
        data = json.loads(request.body)
        try:
            Bidding.objects.filter(
                user_id        = Bidding.objects.filter(productsize__size__name = data['productsize'], price=data['price'])[0].user.id,
                productsize_id = ProductSize.objects.get(product=product_id, size__name=data['productsize']).id,
                bid_type_id    = data['bid_type'],
                price          = data['price'],
            ).delete()
            
            return JsonResponse({'message': "SUCCESS"}, status=204)
 
        except Bidding.DoesNotExist:
            return JsonResponse({"message" : "BIDDING_DOESNOTEXIST"}, status=404)

class OrderListView(View):
    @login_decorator
    def post(self, request, product_id):
        data = json.loads(request.body)
        try:
            if not re.match('^(0|[1-9]+[0-9]*)$',str(data['price'])):
                return JsonResponse({"message": "올바른 가격 정보를 입력해 주세요."})

            if data['bid_type'] == BidType.BUYING:
                Order.objects.create(
                    buyer          = request.user,
                    seller         = Bidding.objects.filter(productsize__size__name = data['productsize'], price=data['price'])[0].user,
                    status         = '거래완료',
                    productsize_id = ProductSize.objects.get(product=product_id, size__name=data['productsize']).id,
                    price          = data['price'],
                ) 

                return JsonResponse({'message': "SUCCESS"}, status=201)
                
            else:
                Order.objects.create(
                    buyer          = Bidding.objects.filter(productsize__size__name = data['productsize'], price=data['price'])[0].user,
                    seller         = request.user,
                    status         = '거래완료',
                    productsize_id = ProductSize.objects.get(product=product_id, size__name=data['productsize']).id,
                    price          = data['price'],
                ) 

                return JsonResponse({'message': "SUCCESS"}, status=201)
        
        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)