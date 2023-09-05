from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status

from apps.customer.models import Customer
from apps.customer.serializers import CustomerSerializer
from apps.customer.wallet_actions import WalletActions


class LoginView(APIView):
    def post(self, request: Request) -> Response:

        # TODO add validators

        if "user_name" not in request.data or "password" not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        customers = Customer.objects.filter(
            user_name=request.data["user_name"], password=request.data["password"])

        if len(customers) != 1:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        customers_serializer = CustomerSerializer(customers[0])

        return Response(data=customers_serializer.data)


class AddMoneyView(APIView):
    def post(self, request: Request) -> Response:

        result = WalletActions().addMoney(
            request.data['customer_id'], request.data['amount'])

        return Response(data=result)


class RefundView(APIView):
    def post(self, request: Request) -> Response:

        result = WalletActions().refund(request.data['customer_id'])

        return Response(data=result)
