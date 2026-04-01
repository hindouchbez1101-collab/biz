from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ("clinic", "0002_doctor_payer_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="Supplier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True)),
                ("phone", models.CharField(blank=True, default="", max_length=60)),
                ("address", models.CharField(blank=True, default="", max_length=255)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=200, unique=True)),
                ("role", models.CharField(blank=True, default="", max_length=120)),
                ("phone", models.CharField(blank=True, default="", max_length=60)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["full_name"]},
        ),
        migrations.CreateModel(
            name="Purchase",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("invoice_no", models.CharField(blank=True, default="", max_length=60)),
                ("purchased_at", models.DateField()),
                ("status", models.CharField(choices=[("DRAFT", "Brouillon"), ("PENDING", "En attente validation"), ("APPROVED", "Validé"), ("RECEIVED", "Réceptionné"), ("PAID", "Payé"), ("CANCELLED", "Annulé")], default="PENDING", max_length=12)),
                ("note", models.CharField(blank=True, default="", max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("approved_at", models.DateTimeField(blank=True, null=True)),
                ("total_amount", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("approved_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="approved_purchases", to=settings.AUTH_USER_MODEL)),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="created_purchases", to=settings.AUTH_USER_MODEL)),
                ("supplier", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="purchases", to="clinic.supplier")),
            ],
            options={"ordering": ["-purchased_at", "-created_at"]},
        ),
        migrations.CreateModel(
            name="PurchaseItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(max_length=200)),
                ("qty", models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ("unit_price", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("line_total", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("purchase", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="clinic.purchase")),
            ],
        ),
        migrations.CreateModel(
            name="Salary",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("month", models.DateField(help_text="Utiliser le 1er jour du mois (ex: 2026-02-01)")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("paid_at", models.DateField(blank=True, null=True)),
                ("note", models.CharField(blank=True, default="", max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="created_salaries", to=settings.AUTH_USER_MODEL)),
                ("employee", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="salaries", to="clinic.employee")),
            ],
            options={"ordering": ["-month", "employee__full_name"], "unique_together": {("employee", "month")}},
        ),
    ]
