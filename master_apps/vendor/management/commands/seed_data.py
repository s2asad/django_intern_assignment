from django.core.management.base import BaseCommand
from master_apps.vendor.models import Vendor
from master_apps.product.models import Product
from master_apps.course.models import Course
from master_apps.certification.models import Certification
from mapping_apps.vendor_product_mapping.models import VendorProductMapping
from mapping_apps.product_course_mapping.models import ProductCourseMapping
from mapping_apps.course_certification_mapping.models import CourseCertificationMapping


class Command(BaseCommand):
    help = "Seed the database with rich sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Seeding data... please wait"))

        # ── VENDORS ──────────────────────────────────────────────
        vendors_data = [
            {"code": "VND001", "name": "TechNova Solutions",      "description": "Enterprise technology solutions provider specializing in cloud and AI."},
            {"code": "VND002", "name": "EduBridge Academy",        "description": "Leading online education platform for professional upskilling."},
            {"code": "VND003", "name": "SkillForge Institute",     "description": "Industry-focused skill development and certification body."},
            {"code": "VND004", "name": "CloudMatrix Corp",         "description": "Cloud infrastructure and DevOps consulting firm."},
            {"code": "VND005", "name": "DataSphere Analytics",     "description": "Data science and machine learning training provider."},
            {"code": "VND006", "name": "SecureNet Training",       "description": "Cybersecurity education and certification partner."},
            {"code": "VND007", "name": "AgileWorks Consulting",    "description": "Agile methodology and project management training."},
            {"code": "VND008", "name": "GreenCode Academy",        "description": "Sustainable software engineering and green IT programs."},
        ]
        vendors = {}
        for d in vendors_data:
            obj, created = Vendor.objects.get_or_create(code=d["code"], defaults={"name": d["name"], "description": d["description"]})
            vendors[d["code"]] = obj
            status = "Created" if created else "Exists "
            self.stdout.write(f"  [{status}] Vendor: {obj.name}")

        # ── PRODUCTS ─────────────────────────────────────────────
        products_data = [
            {"code": "PRD001", "name": "Python Programming Suite",        "description": "Complete Python development training bundle from beginner to advanced."},
            {"code": "PRD002", "name": "Django Web Development Pack",     "description": "Full-stack web development using Django REST Framework and React."},
            {"code": "PRD003", "name": "Cloud & DevOps Bootcamp",         "description": "Hands-on training in AWS, Docker, Kubernetes, and CI/CD pipelines."},
            {"code": "PRD004", "name": "Data Science Fundamentals",       "description": "Core data science skills including statistics, pandas, and visualization."},
            {"code": "PRD005", "name": "Machine Learning Mastery",        "description": "ML algorithms, model training, evaluation, and deployment."},
            {"code": "PRD006", "name": "Cybersecurity Essentials",        "description": "Network security, ethical hacking, and compliance fundamentals."},
            {"code": "PRD007", "name": "Agile & Scrum Practitioner",      "description": "Agile frameworks, Scrum ceremonies, and backlog management."},
            {"code": "PRD008", "name": "React & Frontend Engineering",    "description": "Modern frontend development with React, TypeScript, and Tailwind."},
            {"code": "PRD009", "name": "Database Design & SQL Mastery",   "description": "Relational database design, advanced SQL, and query optimization."},
            {"code": "PRD010", "name": "AI Foundations Program",          "description": "Introduction to artificial intelligence concepts and practical applications."},
        ]
        products = {}
        for d in products_data:
            obj, created = Product.objects.get_or_create(code=d["code"], defaults={"name": d["name"], "description": d["description"]})
            products[d["code"]] = obj
            status = "Created" if created else "Exists "
            self.stdout.write(f"  [{status}] Product: {obj.name}")

        # ── COURSES ──────────────────────────────────────────────
        courses_data = [
            {"code": "CRS001", "name": "Python Basics",                   "description": "Variables, data types, loops, functions, and OOP in Python."},
            {"code": "CRS002", "name": "Python Intermediate",             "description": "File handling, decorators, generators, and standard library."},
            {"code": "CRS003", "name": "Python Advanced",                 "description": "Metaclasses, async programming, performance tuning, and testing."},
            {"code": "CRS004", "name": "Django Fundamentals",             "description": "Models, views, templates, URL routing, and admin interface."},
            {"code": "CRS005", "name": "Django REST Framework",           "description": "APIView, serializers, authentication, permissions, and Swagger docs."},
            {"code": "CRS006", "name": "AWS Cloud Practitioner",          "description": "Core AWS services: EC2, S3, RDS, IAM, and the shared responsibility model."},
            {"code": "CRS007", "name": "Docker & Kubernetes",             "description": "Containerization, orchestration, Helm charts, and production deployments."},
            {"code": "CRS008", "name": "Data Analysis with Pandas",       "description": "DataFrame operations, data cleaning, merging, and exploratory analysis."},
            {"code": "CRS009", "name": "Machine Learning with Scikit-Learn", "description": "Regression, classification, clustering, and model evaluation techniques."},
            {"code": "CRS010", "name": "Deep Learning with TensorFlow",   "description": "Neural networks, CNNs, RNNs, and model deployment with TF Serving."},
            {"code": "CRS011", "name": "Ethical Hacking",                 "description": "Penetration testing, vulnerability scanning, and exploit development."},
            {"code": "CRS012", "name": "Network Security Fundamentals",   "description": "Firewalls, VPNs, intrusion detection, and secure network architecture."},
            {"code": "CRS013", "name": "Scrum Master Certification Prep", "description": "Scrum events, artifacts, roles, and team dynamics."},
            {"code": "CRS014", "name": "React for Beginners",             "description": "JSX, components, state, props, hooks, and React Router."},
            {"code": "CRS015", "name": "Advanced SQL & Query Tuning",     "description": "Window functions, CTEs, indexes, execution plans, and optimizations."},
        ]
        courses = {}
        for d in courses_data:
            obj, created = Course.objects.get_or_create(code=d["code"], defaults={"name": d["name"], "description": d["description"]})
            courses[d["code"]] = obj
            status = "Created" if created else "Exists "
            self.stdout.write(f"  [{status}] Course: {obj.name}")

        # ── CERTIFICATIONS ────────────────────────────────────────
        certifications_data = [
            {"code": "CERT001", "name": "Certified Python Developer",          "description": "Validates proficiency in Python programming and software design patterns."},
            {"code": "CERT002", "name": "Certified Django Professional",        "description": "Recognizes expertise in building production-grade Django REST APIs."},
            {"code": "CERT003", "name": "AWS Certified Cloud Practitioner",     "description": "Entry-level AWS certification covering cloud concepts and core services."},
            {"code": "CERT004", "name": "Certified Kubernetes Administrator",   "description": "Validates skills in deploying, scaling, and managing Kubernetes clusters."},
            {"code": "CERT005", "name": "Data Science Professional Certificate","description": "Industry recognition for data wrangling, visualization, and ML skills."},
            {"code": "CERT006", "name": "TensorFlow Developer Certificate",     "description": "Google-endorsed certification for deep learning with TensorFlow."},
            {"code": "CERT007", "name": "Certified Ethical Hacker (CEH)",       "description": "Globally recognized credential for offensive security professionals."},
            {"code": "CERT008", "name": "CompTIA Security+",                    "description": "Vendor-neutral certification for cybersecurity best practices and risk management."},
            {"code": "CERT009", "name": "Certified ScrumMaster (CSM)",          "description": "Scrum Alliance certification for Scrum Masters facilitating agile teams."},
            {"code": "CERT010", "name": "Meta Frontend Developer Certificate",  "description": "Meta-backed certification for React and modern frontend engineering."},
            {"code": "CERT011", "name": "Oracle SQL Certified Associate",       "description": "SQL fundamentals and database design certification from Oracle."},
            {"code": "CERT012", "name": "AI Practitioner Badge",                "description": "Foundational badge recognizing understanding of AI concepts and applications."},
        ]
        certifications = {}
        for d in certifications_data:
            obj, created = Certification.objects.get_or_create(code=d["code"], defaults={"name": d["name"], "description": d["description"]})
            certifications[d["code"]] = obj
            status = "Created" if created else "Exists "
            self.stdout.write(f"  [{status}] Certification: {obj.name}")

        # ── VENDOR → PRODUCT MAPPINGS ─────────────────────────────
        self.stdout.write(self.style.WARNING("\nCreating Vendor → Product mappings..."))
        vp_mappings = [
            # vendor_code,  product_code,  primary
            ("VND001", "PRD001", True),
            ("VND001", "PRD002", False),
            ("VND001", "PRD010", False),
            ("VND002", "PRD003", True),
            ("VND002", "PRD004", False),
            ("VND002", "PRD007", False),
            ("VND003", "PRD005", True),
            ("VND003", "PRD006", False),
            ("VND004", "PRD003", False),
            ("VND004", "PRD009", True),
            ("VND005", "PRD004", True),
            ("VND005", "PRD005", False),
            ("VND005", "PRD010", False),
            ("VND006", "PRD006", True),
            ("VND007", "PRD007", True),
            ("VND008", "PRD008", True),
            ("VND008", "PRD001", False),
        ]
        for vc, pc, primary in vp_mappings:
            obj, created = VendorProductMapping.objects.get_or_create(
                vendor=vendors[vc], product=products[pc],
                defaults={"primary_mapping": primary}
            )
            status = "Created" if created else "Exists "
            self.stdout.write(f"  [{status}] {vendors[vc].name} → {products[pc].name} (primary={primary})")

        # ── PRODUCT → COURSE MAPPINGS ─────────────────────────────
        self.stdout.write(self.style.WARNING("\nCreating Product → Course mappings..."))
        pc_mappings = [
            ("PRD001", "CRS001", True),
            ("PRD001", "CRS002", False),
            ("PRD001", "CRS003", False),
            ("PRD002", "CRS004", True),
            ("PRD002", "CRS005", False),
            ("PRD003", "CRS006", True),
            ("PRD003", "CRS007", False),
            ("PRD004", "CRS008", True),
            ("PRD005", "CRS009", True),
            ("PRD005", "CRS010", False),
            ("PRD006", "CRS011", True),
            ("PRD006", "CRS012", False),
            ("PRD007", "CRS013", True),
            ("PRD008", "CRS014", True),
            ("PRD009", "CRS015", True),
            ("PRD010", "CRS009", False),
            ("PRD010", "CRS010", True),
        ]
        for pc, cc, primary in pc_mappings:
            obj, created = ProductCourseMapping.objects.get_or_create(
                product=products[pc], course=courses[cc],
                defaults={"primary_mapping": primary}
            )
            status = "Created" if created else "Exists "
            self.stdout.write(f"  [{status}] {products[pc].name} → {courses[cc].name} (primary={primary})")

        # ── COURSE → CERTIFICATION MAPPINGS ──────────────────────
        self.stdout.write(self.style.WARNING("\nCreating Course → Certification mappings..."))
        cc_mappings = [
            ("CRS001", "CERT001", True),
            ("CRS002", "CERT001", False),
            ("CRS003", "CERT001", False),
            ("CRS004", "CERT002", True),
            ("CRS005", "CERT002", False),
            ("CRS006", "CERT003", True),
            ("CRS007", "CERT004", True),
            ("CRS008", "CERT005", True),
            ("CRS009", "CERT005", False),
            ("CRS010", "CERT006", True),
            ("CRS011", "CERT007", True),
            ("CRS012", "CERT008", True),
            ("CRS013", "CERT009", True),
            ("CRS014", "CERT010", True),
            ("CRS015", "CERT011", True),
            ("CRS009", "CERT012", False),
            ("CRS010", "CERT012", False),
        ]
        for cc, certc, primary in cc_mappings:
            obj, created = CourseCertificationMapping.objects.get_or_create(
                course=courses[cc], certification=certifications[certc],
                defaults={"primary_mapping": primary}
            )
            status = "Created" if created else "Exists "
            self.stdout.write(f"  [{status}] {courses[cc].name} → {certifications[certc].name} (primary={primary})")

        # ── SUMMARY ───────────────────────────────────────────────
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 55))
        self.stdout.write(self.style.SUCCESS("  Seed complete! Summary:"))
        self.stdout.write(self.style.SUCCESS(f"    Vendors        : {Vendor.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"    Products       : {Product.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"    Courses        : {Course.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"    Certifications : {Certification.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"    VP Mappings    : {VendorProductMapping.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"    PC Mappings    : {ProductCourseMapping.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"    CC Mappings    : {CourseCertificationMapping.objects.count()}"))
        self.stdout.write(self.style.SUCCESS("=" * 55))
