from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer
from core.utils import success_response, error_response, not_found_response


class VendorProductMappingListCreateView(APIView):

    @swagger_auto_schema(
        operation_description="List vendor-product mappings. Filter by vendor_id or product_id.",
        manual_parameters=[
            openapi.Parameter("vendor_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter by vendor ID"),
            openapi.Parameter("product_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter by product ID"),
        ],
        responses={200: VendorProductMappingSerializer(many=True)},
    )
    def get(self, request):
        mappings = VendorProductMapping.objects.all()
        vendor_id = request.query_params.get("vendor_id")
        product_id = request.query_params.get("product_id")
        if vendor_id:
            mappings = mappings.filter(vendor_id=vendor_id)
        if product_id:
            mappings = mappings.filter(product_id=product_id)
        serializer = VendorProductMappingSerializer(mappings, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a vendor-product mapping",
        request_body=VendorProductMappingSerializer,
        responses={201: VendorProductMappingSerializer, 400: "Validation error"},
    )
    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response("Validation failed.", errors=serializer.errors)


class VendorProductMappingDetailView(APIView):

    def get_object(self, pk):
        try:
            return VendorProductMapping.objects.get(pk=pk)
        except VendorProductMapping.DoesNotExist:
            return None

    @swagger_auto_schema(operation_description="Retrieve a vendor-product mapping", responses={200: VendorProductMappingSerializer})
    def get(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return not_found_response("VendorProductMapping")
        return success_response(VendorProductMappingSerializer(mapping).data)

    @swagger_auto_schema(operation_description="Update a vendor-product mapping", request_body=VendorProductMappingSerializer)
    def put(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return not_found_response("VendorProductMapping")
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Partial update a vendor-product mapping", request_body=VendorProductMappingSerializer)
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return not_found_response("VendorProductMapping")
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Soft delete a vendor-product mapping")
    def delete(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return not_found_response("VendorProductMapping")
        mapping.is_active = False
        mapping.save()
        return success_response({"detail": "Mapping deactivated successfully."})
