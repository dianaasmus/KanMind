from user_auth_app.models import UserProfile
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get("email")

        if email:
            try:
                user = User.objects.get(email=email)
                request.data["username"] = user.username
            except User.DoesNotExist:
                return Response({"error": "Falsche E-Mail oder Passwort."}, status=400)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            response_data = {
                "token": token.key,
                "fullname": f"{user.first_name} {user.last_name}".strip(),
                "email": user.email,
                "user_id": user.id,
            }
            return Response(response_data, status=201)

        return Response(serializer.errors, status=400)


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
            saved_account.first_name = data["first_name"]
            saved_account.last_name = data["last_name"]
            saved_account.save()
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
