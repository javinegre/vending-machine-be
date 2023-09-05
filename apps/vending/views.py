from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.vending.models import VendingMachineSlot
from apps.vending.serializers import VendingMachineSlotSerializer
from apps.vending.validators import ListSlotsValidator

from apps.vending.constants import VENDING_MACHINE_MAX_COLUMNS, VENDING_MACHINE_MAX_ROWS
from apps.vending.product_order import OrderMissingResourceError, ProductOrder
from rest_framework import status


class VendingMachineSlotView(APIView):
    def get(self, request: Request) -> Response:
        validator = ListSlotsValidator(data=request.query_params)
        validator.is_valid(raise_exception=True)
        filters = {}
        if quantity := validator.validated_data["quantity"]:
            filters["quantity__lte"] = quantity

        slots = VendingMachineSlot.objects.filter(**filters)

        # initialize grid with empty items
        slots_grid = [[None for _ in range(
            VENDING_MACHINE_MAX_COLUMNS)] for _ in range(VENDING_MACHINE_MAX_ROWS)]

        for slot in slots:
            slots_grid[slot.row-1][slot.column -
                                   1] = VendingMachineSlotSerializer(slot).data

        # slots_serializer = VendingMachineSlotSerializer(slots, many=True)
        return Response(data=slots_grid)


class ProductOrderView(APIView):
    def post(self, request: Request) -> Response:
        try:
            result = ProductOrder().buy(
                request.data['customer_id'], request.data['slot_id'], request.data['price'])
        except OrderMissingResourceError as ex:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": ex.message})

        return Response(data=result)
