from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product
from .serializers import ProductSerializer, ProductNestedSerializer
from core.utils import success_response, error_response, not_found_response


class ProductListCreateView(APIView):

    @swagger_auto_schema(
        operation_description="List all products.",
        manual_parameters=[
            openapi.Parameter("is_active", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request):
        products = Product.objects.all()
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            products = products.filter(is_active=is_active.lower() == "true")
        return success_response(ProductSerializer(products, many=True).data)

    @swagger_auto_schema(operation_description="Create a product", request_body=ProductSerializer, responses={201: ProductSerializer})
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response("Validation failed.", errors=serializer.errors)


class ProductDetailView(APIView):

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    @swagger_auto_schema(operation_description="Retrieve a product", responses={200: ProductSerializer})
    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return not_found_response("Product")
        return success_response(ProductSerializer(product).data)

    @swagger_auto_schema(operation_description="Update a product", request_body=ProductSerializer)
    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return not_found_response("Product")
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Partial update a product", request_body=ProductSerializer)
    def patch(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return not_found_response("Product")
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Soft delete a product")
    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return not_found_response("Product")
        product.is_active = False
        product.save()
        return success_response({"detail": "Product deactivated successfully."})


class ProductNestedView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a product with all its mapped courses (nested response)",
        responses={200: ProductNestedSerializer},
    )
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return not_found_response("Product")
        return success_response(ProductNestedSerializer(product).data)
