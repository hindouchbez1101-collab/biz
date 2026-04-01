# Generated manually for initial setup (Clinique Cerine Alaa-Med)
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=120)),
                ("last_name", models.CharField(max_length=120)),
                ("phone", models.CharField(max_length=40, unique=True)),
                ("birth_date", models.DateField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["last_name", "first_name"]},
        ),
        migrations.CreateModel(
            name="LabTest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="LabPack",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("tests", models.ManyToManyField(blank=True, related_name="packs", to="clinic.labtest")),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Expense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("category", models.CharField(choices=[("LOYER", "Loyer"), ("SALAIRE", "Salaire"), ("MATERIEL", "Matériel"), ("INTERNET", "Internet"), ("MAINTENANCE", "Maintenance"), ("AUTRE", "Autre")], max_length=30)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("spent_at", models.DateField()),
                ("note", models.CharField(blank=True, default="", max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="created_expenses", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-spent_at", "-created_at"]},
        ),
        migrations.CreateModel(
            name="Appointment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_at", models.DateTimeField()),
                ("service_type", models.CharField(choices=[("CONSULT", "Consultation"), ("ECHO", "Échographie"), ("NAT", "Accouchement naturel"), ("CES", "Césarienne"), ("LAB", "Analyses"), ("OTHER", "Autre")], max_length=12)),
                ("status", models.CharField(choices=[("PENDING", "En attente"), ("CONFIRMED", "Confirmé"), ("CANCELLED", "Annulé"), ("DONE", "Terminé")], default="CONFIRMED", max_length=12)),
                ("note", models.CharField(blank=True, default="", max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="created_appointments", to=settings.AUTH_USER_MODEL)),
                ("patient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="appointments", to="clinic.patient")),
            ],
            options={"ordering": ["-start_at"]},
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("service_type", models.CharField(choices=[("CONSULT", "Consultation"), ("ECHO", "Échographie"), ("NAT", "Accouchement naturel"), ("CES", "Césarienne"), ("LAB", "Analyses"), ("OTHER", "Autre")], max_length=12)),
                ("amount_total", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("note", models.CharField(blank=True, default="", max_length=255)),
                ("receipt_no", models.CharField(max_length=30, unique=True)),
                ("paid_at", models.DateTimeField(auto_now_add=True)),
                ("appointment", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="payments", to="clinic.appointment")),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="created_payments", to=settings.AUTH_USER_MODEL)),
                ("patient", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="payments", to="clinic.patient")),
            ],
            options={"ordering": ["-paid_at"]},
        ),
        migrations.CreateModel(
            name="PaymentItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, default="", max_length=200)),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("lab_test", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="clinic.labtest")),
                ("payment", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="clinic.payment")),
            ],
        ),
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action", models.CharField(max_length=80)),
                ("entity", models.CharField(max_length=80)),
                ("entity_id", models.CharField(blank=True, default="", max_length=40)),
                ("message", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("actor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
