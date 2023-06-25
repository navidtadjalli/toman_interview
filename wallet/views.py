from http import HTTPStatus

from rest_framework import generics
from rest_framework.response import Response


class DepositAPIView(generics.GenericAPIView):
    def post(self, request):
        return Response({
            "amount": "",
            "lock_time": ""
        }, status=HTTPStatus.BAD_REQUEST)
