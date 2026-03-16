from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Vendor
from .serializers import VendorSerializer, VendorNestedSerializer
from core.utils import success_response, error_response, not_found_response


class VendorListCreateView(APIView):

    @swagger_auto_schema(
        operation_description="List all vendors. Use ?is_active=true to filter active only.",
        manual_parameters=[
            openapi.Parameter("is_active", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description="Filter by active status"),
        ],
        responses={200: VendorSerializer(many=True)},
    )
    def get(self, request):
        vendors = Vendor.objects.all()
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            vendors = vendors.filter(is_active=is_active.lower() == "true")
        serializer = VendorSerializer(vendors, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new vendor",
        request_body=VendorSerializer,
        responses={201: VendorSerializer, 400: "Validation error"},
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response("Validation failed.", errors=serializer.errors)


class VendorDetailView(APIView):

    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return None

    @swagger_auto_schema(operation_description="Retrieve a vendor", responses={200: VendorSerializer})
    def get(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return not_found_response("Vendor")
        return success_response(VendorSerializer(vendor).data)

    @swagger_auto_schema(operation_description="Update a vendor", request_body=VendorSerializer)
    def put(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return not_found_response("Vendor")
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Partial update a vendor", request_body=VendorSerializer)
    def patch(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return not_found_response("Vendor")
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Soft delete a vendor (sets is_active=False)")
    def delete(self, request, pk):
        vendor = self.get_object(pk)
        if not vendor:
            return not_found_response("Vendor")
        vendor.is_active = False
        vendor.save()
        return success_response({"detail": "Vendor deactivated successfully."})


class VendorNestedView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a vendor with all its mapped products (nested response)",
        responses={200: VendorNestedSerializer},
    )
    def get(self, request, pk):
        try:
            vendor = Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return not_found_response("Vendor")
        return success_response(VendorNestedSerializer(vendor).data)
