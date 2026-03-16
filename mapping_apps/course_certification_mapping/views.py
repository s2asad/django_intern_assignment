from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer
from core.utils import success_response, error_response, not_found_response


class CourseCertificationMappingListCreateView(APIView):

    @swagger_auto_schema(
        operation_description="List course-certification mappings. Filter by course_id or certification_id.",
        manual_parameters=[
            openapi.Parameter("course_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter by course ID"),
            openapi.Parameter("certification_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter by certification ID"),
        ],
        responses={200: CourseCertificationMappingSerializer(many=True)},
    )
    def get(self, request):
        mappings = CourseCertificationMapping.objects.all()
        course_id = request.query_params.get("course_id")
        certification_id = request.query_params.get("certification_id")
        if course_id:
            mappings = mappings.filter(course_id=course_id)
        if certification_id:
            mappings = mappings.filter(certification_id=certification_id)
        serializer = CourseCertificationMappingSerializer(mappings, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={201: CourseCertificationMappingSerializer},
    )
    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response("Validation failed.", errors=serializer.errors)


class CourseCertificationMappingDetailView(APIView):

    def get_object(self, pk):
        try:
            return CourseCertificationMapping.objects.get(pk=pk)
        except CourseCertificationMapping.DoesNotExist:
            return None

    @swagger_auto_schema(operation_description="Retrieve a course-certification mapping", responses={200: CourseCertificationMappingSerializer})
    def get(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return not_found_response("CourseCertificationMapping")
        return success_response(CourseCertificationMappingSerializer(mapping).data)

    @swagger_auto_schema(operation_description="Update a course-certification mapping", request_body=CourseCertificationMappingSerializer)
    def put(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return not_found_response("CourseCertificationMapping")
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Partial update a course-certification mapping", request_body=CourseCertificationMappingSerializer)
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return not_found_response("CourseCertificationMapping")
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Soft delete a course-certification mapping")
    def delete(self, request, pk):
        mapping = self.get_object(pk)
        if not mapping:
            return not_found_response("CourseCertificationMapping")
        mapping.is_active = False
        mapping.save()
        return success_response({"detail": "Mapping deactivated successfully."})
