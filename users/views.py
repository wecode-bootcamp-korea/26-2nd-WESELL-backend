import requests, jwt

from django.http.response import JsonResponse
from django.conf          import settings
from django.views         import View

from users.models import User

class KakaoSignInView(View):
    def get(self, request):
        try:
            kakao_token = request.headers['Authorization']

            response = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization': f'Bearer {kakao_token}'})

            if response.json().get("code") == -401 :
                return JsonResponse({"MESSAGE" : "INVALD_TOKEN"}, status=401)

            kakao_id    = response.json()['id']
            kakao_email = response.json()['kakao_account']['email']

            user, created = User.objects.get_or_create(
                kakao = kakao_id,
                email = kakao_email
            )

            access_token     = jwt.encode({'id': user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
            http_status_code = 201 if created else 200

            return JsonResponse({'access_token': access_token}, status=http_status_code)
        
        except KeyError:
            return JsonResponse({'message': 'AUTHORIZATION_KEY_ERROR'}, status=400)