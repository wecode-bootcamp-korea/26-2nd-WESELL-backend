import json

from django.test import TestCase, Client

from freezegun import freeze_time

from products.models import Brand, Product, Size, ProductSize, ProductImage, Category
from biddings.models import Order, Bidding, BidType
from users.models    import User

class ProductDetailTest(TestCase):
    @freeze_time('2021-11-01')
    def setUp(self):
        self.maxDiff = None
        Brand.objects.bulk_create([
            Brand(
                id   = 1,
                name = 'Jordan'
            ),
            Brand(
                id   = 2,
                name = 'Nike'
            ),
            Brand(
                id   = 3,
                name = 'New Balance'
            ),
            Brand(
                id   = 4,
                name = 'Adidas'
            ),
            Brand(
                id   = 5,
                name = 'Vans'
            ),
        ])

        Category.objects.bulk_create([
            Category(
                id   = 1,
                name = '패션소품'
            ),
            Category(
                id   = 2,
                name = '의류'
            ),
            Category(
                id   = 3,
                name = '테크'
            ),
            Category(
                id   = 4,
                name = '스니커즈'
            ),
            Category(
                id   = 5,
                name = '라이프'
            ),
        ])
        
        Size.objects.bulk_create([
            Size(
                id   = 1,
                name = 230),
            Size(
                id   = 2,
                name = 240),
            Size(
                id   = 3,
                name = 250),
            Size(
                id   = 4,
                name = 260),
            Size(
                id   = 5,
                name = 270),
        ])

        User.objects.bulk_create([
            User(
                id         = 1,
                kakao      = '',
                email      = 'kim@naver.com',
                size       = '270',
                created_at = '2021-11-17 11:57:45.004767',
                updated_at = '2021-11-17 11:57:45.004846'
            ),
            User(
                id         = 2,
                kakao      = '',
                email      = 'lee@naver.com',
                size       = '230',
                created_at = '2021-11-17 11:57:45.025797',
                updated_at = '2021-11-17 11:57:45.025849'
            ),
            User(
                id         = 3,
                kakao      = '',
                email      = 'park@naver.com',
                size       = '240',
                created_at = '2021-11-17 11:57:45.038242',
                updated_at = '2021-11-17 11:57:45.038296'
            ),
            User(
                id         = 4,
                kakao      = '',
                email      = 'choi@naver.com',
                size       = '250',
                created_at = '2021-11-17 11:57:45.050985',
                updated_at = '2021-11-17 11:57:45.051046'
            )
        ])

        BidType.objects.bulk_create([
            BidType(
                id   = 1,
                name = 'Buy'
            ),
            BidType(
                id   = 2,
                name = 'Sell'
            )
        ])

        Product.objects.bulk_create([
            Product(
                id = 1,
                en_name       = 'Jordan 1 Retro High OG Bordeaux',
                ko_name       = '조던 1 레트로 하이 OG 보르도',
                model_number  = '555088-611',
                color         = 'BORDEAUX/WHITE-METALLIC SILVER',
                release_date  = '2021-11-15',
                release_price = 199000,
                category_id   = 4,
                brand_id      = 1,
                fast_shipping = True
            ),
            Product(
                id            = 2,
                en_name       = 'Nike Dunk Low Retro Black',
                ko_name       = '나이키 덩크 로우 레트로 블랙',
                model_number  = 'DD1391-100',
                color         = 'WHITE/BLACK',
                release_date  = '2021-01-14',
                release_price =119000,
                category_id   = 4,
                brand_id      = 2,
                fast_shipping = True
            ),
            Product(
                id            = 3,
                en_name       = 'New Balance 327 White Black',
                ko_name       = '뉴발란스 327 화이트 블랙',
                model_number  = 'MS327FE',
                color         = 'SEA SALT/BLACK',
                release_date  = '2021-01-15',
                release_price = 109000,
                category_id   = 4,
                brand_id      = 3,
                fast_shipping = False
            )
        ])

        ProductSize.objects.bulk_create([
            ProductSize(
                id         = 1,
                product_id = 1,
                size_id    = 1
            ),
            ProductSize(
                id         = 2,
                product_id = 1,
                size_id    = 2
            ),
            ProductSize(
                id         = 3,
                product_id = 1,
                size_id    = 3
            ),
            ProductSize(
                id         = 4,
                product_id = 1,
                size_id    = 4
            ),
            ProductSize(
                id         = 5,
                product_id = 1,
                size_id    = 5
            ),
            ProductSize(
                id         = 6,
                product_id = 2,
                size_id    = 1
            ),
            ProductSize(
                id         = 7,
                product_id = 2,
                size_id    = 2
            ),
            ProductSize(
                id         = 8,
                product_id = 2,
                size_id    = 3
            ),
            ProductSize(
                id         = 9,
                product_id = 2,
                size_id    = 4
            ),
            ProductSize(
                id         = 10,
                product_id = 2,
                size_id    = 5
            ),
            ProductSize(
                id         = 11,
                product_id = 3,
                size_id    = 1
            ),
            ProductSize(
                id         = 12,
                product_id = 3,
                size_id    = 2
            ),
            ProductSize(
                id         = 13,
                product_id = 3,
                size_id    = 3
            ),
            ProductSize(
                id         = 14,
                product_id = 3,
                size_id    = 4
            ),
            ProductSize(
                id         = 15,
                product_id = 3,
                size_id    = 5
            ),
        ])

        Order.objects.bulk_create([
            Order(
                id             = 1,
                buyer_id       = 1,
                seller_id      = 2,
                status         = '거래완료',
                productsize_id = 1,
                price          = 378000,
                created_at     = '2021-11-01',
                updated_at     = '2021-11-01'
            ),
            Order(
                id             = 2,
                buyer_id       = 2,
                seller_id      = 3,
                status         = '거래완료',
                productsize_id = 1,
                price          = 341000,
                created_at     = '2021-11-01',
                updated_at     = '2021-11-01'
            )
        ])

        Bidding.objects.bulk_create([
            Bidding(
                id             = 1,
                user_id        = 1,
                productsize_id = 1,
                bid_type_id    = 1,
                price          = 335000,
                created_at     = '2021-11-20 08:45:08.061045',
                updated_at     = '2021-11-20 08:45:08.061124'
            ),
            Bidding(
                id             = 2,
                user_id        = 2,
                productsize_id = 1,
                bid_type_id    = 1,
                price          = 327000,
                created_at     = '2021-11-20 08:45:08.066820',
                updated_at     = '2021-11-20 08:45:08.066885'
            ),
            Bidding(
                id             = 3,
                user_id        = 3,
                productsize_id = 1,
                bid_type_id    = 1,
                price          = 345000,
                created_at     = '2021-11-20 08:45:08.070365',
                updated_at     = '2021-11-20 08:45:08.070428'
            ),
            Bidding(
                id             = 4,
                user_id        = 3,
                productsize_id = 1,
                bid_type_id    = 2,
                price          = 354000,
                created_at     = '2021-11-20 08:45:08.119945',
                updated_at     = '2021-11-20 08:45:08.119992'
            ),
            Bidding(
                id             = 5,
                user_id        = 2,
                productsize_id = 1,
                bid_type_id    = 2,
                price          = 365000,
                created_at     = '2021-11-20 08:45:08.123486',
                updated_at     = '2021-11-20 08:45:08.123536'
            ),
            Bidding(
                id             = 6,
                user_id        = 1,
                productsize_id = 1,
                bid_type_id    = 2,
                price          = 380000,
                created_at     = '2021-11-20 08:45:08.126378',
                updated_at     = '2021-11-20 08:45:08.126446'
            ),
            Bidding(
                id             = 7,
                user_id        = 1,
                productsize_id = 2,
                bid_type_id    = 1,
                price          = 335000,
                created_at     = '2021-11-20 08:45:08.061045',
                updated_at     = '2021-11-20 08:45:08.061124'
            ),
            Bidding(
                id             = 8,
                user_id        = 2,
                productsize_id = 2,
                bid_type_id    = 1,
                price          = 329000,
                created_at     = '2021-11-20 08:45:08.066820',
                updated_at     = '2021-11-20 08:45:08.066885'
            ),
            Bidding(
                id             = 9,
                user_id        = 3,
                productsize_id = 2,
                bid_type_id    = 1,
                price          = 345000,
                created_at     = '2021-11-20 08:45:08.070365',
                updated_at     = '2021-11-20 08:45:08.070428'
            ),
            Bidding(
                id             = 10,
                user_id        = 3,
                productsize_id = 2,
                bid_type_id    = 2,
                price          = 356000,
                created_at     = '2021-11-20 08:45:08.119945',
                updated_at     = '2021-11-20 08:45:08.119992'
            ),
            Bidding(
                id             = 11,
                user_id        = 2,
                productsize_id = 2,
                bid_type_id    = 2,
                price          = 365000,
                created_at     = '2021-11-20 08:45:08.123486',
                updated_at     = '2021-11-20 08:45:08.123536'
            ),
            Bidding(
                id             = 12,
                user_id        = 1,
                productsize_id = 2,
                bid_type_id    = 2,
                price          = 380000,
                created_at     = '2021-11-20 08:45:08.126378',
                updated_at     = '2021-11-20 08:45:08.126446'
            )
        ])

        ProductImage.objects.bulk_create([
            ProductImage(
                id         = 1,
                product_id = 1,
                url        = 'https://github.com/Gyubs/project_WESELL_images/blob/main/10_1.jpg?raw=true'
            ),
            ProductImage(
                id         = 2,
                product_id = 1,
                url        = 'https://github.com/Gyubs/project_WESELL_images/blob/main/10_3.jpg?raw=true'
            ),
            ProductImage(
                id         = 3,
                product_id = 2,
                url        = 'https://github.com/Gyubs/project_WESELL_images/blob/main/11_1.jpg?raw=true'
            ),
            ProductImage(
                id         = 4,
                product_id = 2,
                url        = 'https://github.com/Gyubs/project_WESELL_images/blob/main/11_2.jpg?raw=true'
            ),
            ProductImage(
                id         = 5,
                product_id = 3,
                url        = 'https://github.com/Gyubs/project_WESELL_images/blob/main/12_1.jpg?raw=true'
            ),
            ProductImage(
                id         = 6,
                product_id = 3,
                url        = 'https://github.com/Gyubs/project_WESELL_images/blob/main/12_2.jpg?raw=true'
            ),
        ])

    def tearDown(self) :
        Brand.objects.all().delete()
        Product.objects.all().delete()
        ProductSize.objects.all().delete()
        ProductImage.objects.all().delete()
        Category.objects.all().delete()
        Order.objects.all().delete()
        Bidding.objects.all().delete()
        BidType.objects.all().delete()
        User.objects.all().delete()

    def test_product_detail_success(self):
        client   = Client()        		
        response = client.get('/products/1')
        
        self.assertEqual(response.json(),
            {
                'result' : {
                    'product_info': {
                        'brand': 'Jordan',
                        'color': 'BORDEAUX/WHITE-METALLIC SILVER',
                        'en_name': 'Jordan 1 Retro High OG Bordeaux',
                        'fast_shipping': True,
                        'id': 1,
                        'ko_name': '조던 1 레트로 하이 OG 보르도',
                        'model_number': '555088-611',
                        'release_date': '2021-11-15',
                        'release_price': 199000
                    },
                    'lowest_price_by_size': [
                        {
                            "bid_type": "Buy",
                            "sizes": [
                                {
                                'id': 1,
                                'lowest_price': 327000,
                                'size': '230'
                                },
                                {
                                'id': 2,
                                'lowest_price': 329000,
                                'size': '240'
                                }
                            ]
                        },
                        { "bid_type": "Sell",
                            "sizes": [
                                {
                                'id': 1,
                                'lowest_price': 354000,
                                'size': '230'
                                },
                                {
                                'id': 2,
                                'lowest_price': 356000,
                                'size': '240'
                                }
                            ]
                        }
                    ],
                    'product_image': [
                        {
                        'id': 1,
                        'url': 'https://github.com/Gyubs/project_WESELL_images/blob/main/10_1.jpg?raw=true'
                        },
                        {
                        'id': 2,
                        'url': 'https://github.com/Gyubs/project_WESELL_images/blob/main/10_3.jpg?raw=true'
                        }
                    ],
                    'market_price': [
                        {
                            'date': '2021-11-01',
                            'sizes': [
                                {
                                    'avg_price': 359500.0,
                                    'size': '230'
                                }
                            ]
                        }
                    ],
                    'order_history' : [
                        {
                            'id': 1,
                            'price': 378000,
                            'size': '230',
                            'created_at' : '2021-11-01'
                        },
                        {
                            'id': 2,
                            'price': 341000,
                            'size': '230',
                            'created_at' : '2021-11-01'
                        }
                    ]
                }
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_product_detail_no_product(self):
            client   = Client()        		
            response = client.get('/products/20')

            self.assertEqual(response.json(), { "message": "DOES NOT EXISTS" })
            self.assertEqual(response.status_code, 404)