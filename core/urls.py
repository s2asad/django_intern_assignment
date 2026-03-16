from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Modular Entity & Mapping API",
        default_version="v1",
        description="Django REST Framework API using APIView only. Manages Vendors, Products, Courses, Certifications and their mappings.",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Master entity URLs
    path("api/", include("master_apps.vendor.urls")),
    path("api/", include("master_apps.product.urls")),
    path("api/", include("master_apps.course.urls")),
    path("api/", include("master_apps.certification.urls")),

    # Mapping URLs
    path("api/", include("mapping_apps.vendor_product_mapping.urls")),
    path("api/", include("mapping_apps.product_course_mapping.urls")),
    path("api/", include("mapping_apps.course_certification_mapping.urls")),

    # Swagger / ReDoc
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]
