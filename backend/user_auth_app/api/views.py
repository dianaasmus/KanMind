from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class LoginView(APIView):
    pass


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data.copy()

        if "fullname" in data:
            name_parts = data["fullname"].split()
            data["first_name"] = name_parts[0]
            data["last_name"] = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        data["username"] = data["fullname"].replace(" ", "").lower()

        serializer = RegistrationSerializer(data=data)

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)

            user_profile = UserProfile.objects.create(
                user=saved_account, fullname=request.data["fullname"]
            )

            response_data = {
                "token": token.key,
                "fullname": user_profile.fullname,
                "email": saved_account.email,
                "user_id": saved_account.id,
            }
            return Response(response_data, status=201)

        return Response(serializer.errors, status=400)
