# Django Intern Assignment: Modular Entity and Mapping System

A Django REST Framework backend built using **APIView only** for managing Vendors, Products, Courses, Certifications, and their mappings.

---

## Project Structure

```
.
├── core/                          # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── base_model.py              # Shared abstract base models
│   ├── base_serializer.py
│   └── utils.py                   # Shared utility functions
├── vendor/                        # Master app
├── product/                       # Master app
├── course/                        # Master app
├── certification/                 # Master app
├── vendor_product_mapping/        # Mapping app
├── product_course_mapping/        # Mapping app
├── course_certification_mapping/  # Mapping app
├── manage.py
└── requirements.txt
```

Each app contains its own: `models.py`, `serializers.py`, `views.py`, `urls.py`, `admin.py`

---

## Tech Stack

- Python 3.x
- Django
- Django REST Framework
- drf-yasg (Swagger / ReDoc)
- SQLite (default, swap for PostgreSQL in production)

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd django-intern-assignment
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. (Optional) Seed sample data

```bash
python manage.py seed_data
```

### 6. Create a superuser (for Django Admin)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The server will start at: `http://127.0.0.1:8000`

---

## Installed Apps

```python
INSTALLED_APPS = [
    # ...django defaults...
    "rest_framework",
    "drf_yasg",
    # Master apps
    "vendor",
    "product",
    "course",
    "certification",
    # Mapping apps
    "vendor_product_mapping",
    "product_course_mapping",
    "course_certification_mapping",
]
```

---

## API Documentation

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/swagger/` | Swagger UI |
| `http://127.0.0.1:8000/redoc/` | ReDoc UI |
| `http://127.0.0.1:8000/swagger.json` | OpenAPI JSON schema |

---

## API Endpoints

### Master Entities

#### Vendors
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/vendors/` | List all vendors |
| POST | `/api/vendors/` | Create a vendor |
| GET | `/api/vendors/<id>/` | Retrieve a vendor |
| PUT | `/api/vendors/<id>/` | Full update |
| PATCH | `/api/vendors/<id>/` | Partial update |
| DELETE | `/api/vendors/<id>/` | Soft delete (sets is_active=False) |

#### Products
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/products/` | List all products |
| POST | `/api/products/` | Create a product |
| GET | `/api/products/<id>/` | Retrieve a product |
| PUT | `/api/products/<id>/` | Full update |
| PATCH | `/api/products/<id>/` | Partial update |
| DELETE | `/api/products/<id>/` | Soft delete |

#### Courses
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/courses/` | List all courses |
| POST | `/api/courses/` | Create a course |
| GET | `/api/courses/<id>/` | Retrieve a course |
| PUT | `/api/courses/<id>/` | Full update |
| PATCH | `/api/courses/<id>/` | Partial update |
| DELETE | `/api/courses/<id>/` | Soft delete |

#### Certifications
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/certifications/` | List all certifications |
| POST | `/api/certifications/` | Create a certification |
| GET | `/api/certifications/<id>/` | Retrieve a certification |
| PUT | `/api/certifications/<id>/` | Full update |
| PATCH | `/api/certifications/<id>/` | Partial update |
| DELETE | `/api/certifications/<id>/` | Soft delete |

### Mapping Entities

#### Vendor → Product
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/vendor-product-mappings/` | List (filter: `?vendor_id=` or `?product_id=`) |
| POST | `/api/vendor-product-mappings/` | Create mapping |
| GET | `/api/vendor-product-mappings/<id>/` | Retrieve |
| PUT | `/api/vendor-product-mappings/<id>/` | Full update |
| PATCH | `/api/vendor-product-mappings/<id>/` | Partial update |
| DELETE | `/api/vendor-product-mappings/<id>/` | Soft delete |

#### Product → Course
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/product-course-mappings/` | List (filter: `?product_id=` or `?course_id=`) |
| POST | `/api/product-course-mappings/` | Create mapping |
| GET | `/api/product-course-mappings/<id>/` | Retrieve |
| PUT | `/api/product-course-mappings/<id>/` | Full update |
| PATCH | `/api/product-course-mappings/<id>/` | Partial update |
| DELETE | `/api/product-course-mappings/<id>/` | Soft delete |

#### Course → Certification
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/course-certification-mappings/` | List (filter: `?course_id=` or `?certification_id=`) |
| POST | `/api/course-certification-mappings/` | Create mapping |
| GET | `/api/course-certification-mappings/<id>/` | Retrieve |
| PUT | `/api/course-certification-mappings/<id>/` | Full update |
| PATCH | `/api/course-certification-mappings/<id>/` | Partial update |
| DELETE | `/api/course-certification-mappings/<id>/` | Soft delete |

---

## Filtering Examples

```
GET /api/vendor-product-mappings/?vendor_id=1
GET /api/product-course-mappings/?product_id=2
GET /api/course-certification-mappings/?course_id=3
GET /api/vendors/?is_active=true
```

---

## API Request/Response Examples

### Create a Vendor
```http
POST /api/vendors/
Content-Type: application/json

{
  "name": "Acme Corp",
  "code": "ACM001",
  "description": "A reliable vendor",
  "is_active": true
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Acme Corp",
    "code": "ACM001",
    "description": "A reliable vendor",
    "is_active": true,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
}
```

### Create a Vendor → Product Mapping
```http
POST /api/vendor-product-mappings/
Content-Type: application/json

{
  "vendor": 1,
  "product": 1,
  "primary_mapping": true
}
```

---

## Validation Rules

- **Required fields**: `name`, `code` are required on all master entities
- **Unique code**: Each master entity enforces unique `code` field
- **Duplicate mapping prevention**: Same parent-child pair cannot be inserted twice (enforced via `unique_together`)
- **Single primary mapping**: Only one `primary_mapping=True` is allowed per parent entity at each mapping level
- **Soft delete**: DELETE endpoints set `is_active=False` rather than removing the record

---

## Design Decisions

- **APIView only**: All views extend `rest_framework.views.APIView` — no ViewSets, GenericAPIView, mixins, or routers
- **Abstract base models**: `TimeStampedModel` and `MasterModel` in `core/base_model.py` are shared via inheritance
- **Shared utilities**: `core/utils.py` provides `success_response`, `error_response`, `not_found_response` helpers
- **Modular apps**: Each entity lives in its own app for clean separation of concerns
- **Swagger docs**: All APIView methods are decorated with `@swagger_auto_schema` for full documentation
