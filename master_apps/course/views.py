from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Course
from .serializers import CourseSerializer, CourseNestedSerializer
from core.utils import success_response, error_response, not_found_response


class CourseListCreateView(APIView):

    @swagger_auto_schema(
        operation_description="List all courses.",
        manual_parameters=[openapi.Parameter("is_active", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)],
        responses={200: CourseSerializer(many=True)}
    )
    def get(self, request):
        courses = Course.objects.all()
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            courses = courses.filter(is_active=is_active.lower() == "true")
        return success_response(CourseSerializer(courses, many=True).data)

    @swagger_auto_schema(operation_description="Create a course", request_body=CourseSerializer, responses={201: CourseSerializer})
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response("Validation failed.", errors=serializer.errors)


class CourseDetailView(APIView):

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    @swagger_auto_schema(operation_description="Retrieve a course", responses={200: CourseSerializer})
    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return not_found_response("Course")
        return success_response(CourseSerializer(course).data)

    @swagger_auto_schema(operation_description="Update a course", request_body=CourseSerializer)
    def put(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return not_found_response("Course")
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Partial update a course", request_body=CourseSerializer)
    def patch(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return not_found_response("Course")
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Soft delete a course")
    def delete(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return not_found_response("Course")
        course.is_active = False
        course.save()
        return success_response({"detail": "Course deactivated successfully."})


class CourseNestedView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a course with all its mapped certifications (nested response)",
        responses={200: CourseNestedSerializer},
    )
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return not_found_response("Course")
        return success_response(CourseNestedSerializer(course).data)
