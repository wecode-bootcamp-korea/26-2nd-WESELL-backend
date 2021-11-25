from django.http  import JsonResponse
from django.views import View
from core.storages import MyS3Client

from reviews.models import Review, Comment
from core.utils     import login_decorator
from django.conf    import settings

class ReviewListView(View):
    def get(self, request):
        results = [
            {
                'id'         : review.id,
                'user_email' : review.user.email,
                'product'    : {
                    'product_id'      : review.product.id,
                    'product_image'   : review.product.images.first().url,
                    'product_en_name' : review.product.en_name
                },
                'content'    : review.content,
                'image_url'  : review.image_url,
                'created_at' : review.created_at
            } for review in Review.objects.all().select_related('user', 'product')]

        return JsonResponse({'results' : results}, status=200)

class CommentsView(View):
    def get(self, request, review_id):
        if not Review.objects.filter(id=review_id).exists():
            return JsonResponse({'message' : 'DOES NOT EXISTS'}, status=404)

        results = [
            {
                'user_email' : comment.user.email,
                'content'    : comment.content,
                'image_url'  : comment.image_url,
                'created_at' : comment.updated_at,
            } for comment in Comment.objects.filter(review_id=review_id).select_related('user')]

        return JsonResponse({'results' : results}, status=200)

    @login_decorator
    def post(self, request, review_id):
        if not request.POST['content']:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        file = request.FILES.get('filename')

        image_url = None

        if file:
            s3_client = MyS3Client(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_STORAGE_BUCKET_NAME)
            image_url = s3_client.upload(file)

        Comment.objects.create(
            review_id  = review_id,
            user_id    = request.user.id,
            content    = request.POST['content'],
            image_url  = image_url
        )

        return JsonResponse({'message': 'SUCCESS'}, status=201)