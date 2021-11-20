import jwt, time

from functools        import wraps
from django.http      import JsonResponse
from django.conf      import settings
from django.db        import connection, reset_queries

from users.models     import User

def login_decorator(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            request.user = User.objects.get(id=payload['id'])

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 401) 

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

        return func(self, request, *args, **kwargs)

    return wrapper

def query_debugger(func):
    def wrapper(*args, **kwargs):
        try:
            reset_queries()
            settings.DEBUG = True

            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            
            print(f"Function : {func.__name__}")
            print(f'Number of Queries : {len(connection.queries)}')
            print(f'Run time: {(end - start):.2f}s')

        finally:
            settings.DEBUG = False
        return result
    return wrapper