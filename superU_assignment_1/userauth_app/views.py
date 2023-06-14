from rest_framework.views import APIView
from .serializers import UserSerializser
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt, datetime
from django.http import JsonResponse
from .models import UserProfiles
from .serializers import UserProfilesSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class Register(APIView):
    def post(self, request):
        serialiser = UserSerializser(data = request.data)
        serialiser.is_valid(raise_exception=True)
        serialiser.save()

        return Response(serialiser.data)
    
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password): # check_password provided by django
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60), # how long will the token last
            'iat': datetime.datetime.utcnow() # the datetime when the token is created
        }

        token = jwt.encode(payload, 'secret_message', algorithm='HS256') # token generation using JWT

        # using cookie session to store the token key
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True) # not want the frontend to access the token and used by only backend
        response.data = {
            'jwt': token,
        }


        return response
    
@api_view(['GET','POST'])
def users_list(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Not Authenticated')
    
    try:
        payload = jwt.decode(token, 'secret_message', algorithms='HS256')
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!!')

    if request.method == 'GET':
        user_profiles = UserProfiles.objects.all()
        serializer = UserProfilesSerializer(user_profiles, many=True)
        return JsonResponse({'user_profiles': serializer.data})     
       
    if request.method == 'POST':
        serializer = UserProfilesSerializer(data=request.data)
        print('-',request.data, type(request.data))
        if serializer.is_valid():
            print('-',serializer.validated_data['id'], type(serializer.validated_data))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_user_profile(request, id):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Not Authenticated')
    
    try:
        payload = jwt.decode(token, 'secret_message', algorithms='HS256')
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!!')

    if request.method == 'PATCH':
        user_profiles = UserProfiles.objects.get(pk=id)
        serializer = UserProfilesSerializer(user_profiles, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'user_profiles': serializer.data}, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'details':'success',
        }
        return response