from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from firebase_admin import auth, credentials
import firebase_admin
import os
from dotenv import load_dotenv
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from .authentication import FirebaseAuthentication
from rest_framework import status

# Create your views here.

load_dotenv()
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
    "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL"),
})

default_app = firebase_admin.initialize_app(cred)

class CreateUserView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            password = data["password"]
            if len(password) < 8:
                return Response({
                        "error": "This password is too short. It must contain at least 8 characters"},
                        status=status.HTTP_400_BAD_REQUEST,
                )
            user = serializer.save()
            return Response({'email': user.email, 'username': user.username})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(username=username)
            if user.password != password:
                return Response({'msg': 'password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
            if user is not None:
                custom_token = auth.create_custom_token(username)

                # Return the custom token in the response
                return Response({'custom_token': custom_token, 'username': username}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileView(APIView):

    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        username = request.query_params.get("username")

        try:
            user = CustomUser.objects.get(username=username)
        
            response_data = {
                "username": username,
                "email": user.email,
                "full_name": f"{user.first_name}-{user.last_name}",
            }

            return Response(response_data, status=200)

        except:
            return Response({'error': 'User not found'}, status=404)
        

class ProfileUpdateView(APIView):

    authentication_classes = [FirebaseAuthentication]

    def post(self, request):
        username = request.data.get('username')
        new_username = request.data.get('new_username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        old_user = CustomUser.objects.get(username=new_username)
        if old_user:
            return Response({'msg': f'User already exist with the username ${new_username}'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.get(username=username)
        user.username = new_username
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return Response({'email': user.email, 'username': user.username}, status=status.HTTP_200_OK)
