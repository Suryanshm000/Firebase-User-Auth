import os

import firebase_admin
# from django.conf import settings
from django.contrib.auth.models import User
from .models import CustomUser
from django.utils import timezone
from firebase_admin import auth
from firebase_admin import credentials
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from . import exceptions
from dotenv import load_dotenv

# load_dotenv()

# cred = credentials.Certificate(
#     {
#         "type": "service_account",
#         "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
#         "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
#         "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
#         "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
#         "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://accounts.google.com/o/oauth2/token",
#         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#         "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL"),
#     }
# )

# default_app = firebase_admin.initialize_app(cred)


"""FIREBASE AUTHENTICATION"""
class FirebaseAuthentication(BaseAuthentication):

    """override authenticate method and write our custom firebase authentication."""
    def authenticate(self, request):

        """Get the authorization Token, It raise exception when no authorization Token is given"""
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header:
            raise exceptions.NoAuthToken("No auth token provided")
        
        """Decoding the Token It rasie exception when decode failed."""
        id_token = auth_header.split(" ").pop()
        decoded_token = None

        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            print(e)
            raise exceptions.InvalidAuthToken("Invalid auth token")
        
        """Return Nothing"""
        if not id_token or not decoded_token:
            return None
        
        """Get the uid of an user"""
        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise exceptions.FirebaseError()
        
        """Get or create the user"""
        user, created = CustomUser.objects.get_or_create(username=uid)
        return (user, None)