from http import HTTPStatus

from rest_framework import generics
from rest_framework.response import Response

from wallet import serializers


class DepositAPIView(generics.GenericAPIView):
    serializer_class = serializers.DepositSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({}, status=HTTPStatus.OK)
