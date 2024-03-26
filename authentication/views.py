from rest_framework import status
from rest_framework.views import APIView

from authentication import serializers as authentication_serializers
from utils.responses import SuccessAPIResponse, ErrorAPIResponse


class RegisterView(APIView):
    @staticmethod
    def post(request):
        serializer = authentication_serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return SuccessAPIResponse(serializer.data, status=status.HTTP_201_CREATED)
        return ErrorAPIResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @staticmethod
    def post(request):
        serializer = authentication_serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            return SuccessAPIResponse(serializer.data, status=status.HTTP_200_OK)
        return ErrorAPIResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
