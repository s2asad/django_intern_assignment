from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Certification
from .serializers import CertificationSerializer
from core.utils import success_response, error_response, not_found_response


class CertificationListCreateView(APIView):

    @swagger_auto_schema(operation_description="List all certifications", responses={200: CertificationSerializer(many=True)})
    def get(self, request):
        certs = Certification.objects.all()
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            certs = certs.filter(is_active=is_active.lower() == "true")
        serializer = CertificationSerializer(certs, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(operation_description="Create a new certification", request_body=CertificationSerializer, responses={201: CertificationSerializer})
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response("Validation failed.", errors=serializer.errors)


class CertificationDetailView(APIView):

    def get_object(self, pk):
        try:
            return Certification.objects.get(pk=pk)
        except Certification.DoesNotExist:
            return None

    @swagger_auto_schema(operation_description="Retrieve a certification", responses={200: CertificationSerializer})
    def get(self, request, pk):
        cert = self.get_object(pk)
        if not cert:
            return not_found_response("Certification")
        return success_response(CertificationSerializer(cert).data)

    @swagger_auto_schema(operation_description="Update a certification", request_body=CertificationSerializer)
    def put(self, request, pk):
        cert = self.get_object(pk)
        if not cert:
            return not_found_response("Certification")
        serializer = CertificationSerializer(cert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Partial update a certification", request_body=CertificationSerializer)
    def patch(self, request, pk):
        cert = self.get_object(pk)
        if not cert:
            return not_found_response("Certification")
        serializer = CertificationSerializer(cert, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response("Validation failed.", errors=serializer.errors)

    @swagger_auto_schema(operation_description="Soft delete a certification")
    def delete(self, request, pk):
        cert = self.get_object(pk)
        if not cert:
            return not_found_response("Certification")
        cert.is_active = False
        cert.save()
        return success_response({"detail": "Certification deactivated successfully."})
