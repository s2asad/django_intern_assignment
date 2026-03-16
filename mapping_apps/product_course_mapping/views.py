from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer
from core.utils import success_response, error_response, not_found_response


class ProductCourseMappingListCreateView(APIView):

    @swagger_auto_schema(
        operation_description="List product-course mappings. Filter by product_id or course_id.",
        manual_parameters=[
            openapi.Parameter("product_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter by product ID"),
            openapi.Parameter("course_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter by course ID"),
        ],
        responses={200: ProductCourseMappingSerializer(many=True)},
    )
    def get(self, request):
        mappings = ProductCourseMapping.objects.all()
        product_id = request.query_params.get("product_id")
        course_id = request.query_params.get("course_id")
        if product_id:
            mappings = mappings.filter(product_id=product_id)
        if course_id:
            mappings = mappings.filter(course_id=course_id)
        serializer = ProductCourseMappingSerializer(mappings, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a product-course mapping",
        request_body=ProductCourseMappingSerializer,
        responses={201: ProductCourseMappingSerializer},
    )
    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response("Validation failed.", errors=serializer.errors)


class ProductCourseMappingDetailView(APIView):

    def get_object(self, pk):
        try:
            return ProductCourseMapping.objects.get(pk=pk)
        except ProductCourseMapping.DoesNotExist:
            return None

    @swagger_auto_schema(operation_description="Retrieve a product-course mapping", responses={200: ProductCourseMappingSerializer})
    def get(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return not_found_response("ProductCourseMapping")
        return success_response(ProductCourseMappingSerializer(mapping).data)

    @swagger_auto_schema(operation_description="Update a product-course mapping", request_body=ProductCourseMappingSerializer)
    def put(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return not_found_response("ProductCourseMapping")
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Partial update a product-course mapping", request_body=ProductCourseMappingSerializer)
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return not_found_response("ProductCourseMapping")
        serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Soft delete a product-course mapping")
    def delete(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return not_found_response("ProductCourseMapping")
        mapping.is_active = False
        mapping.save()
        return success_response({"detail": "Mapping deactivated successfully."})
