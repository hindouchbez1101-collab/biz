from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ("clinic", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=160, unique=True)),
                ("specialty", models.CharField(blank=True, default="", max_length=120)),
            ],
            options={"ordering": ["full_name"]},
        ),
        migrations.AddField(
            model_name="appointment",
            name="doctor",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="appointments", to="clinic.doctor"),
        ),
        migrations.AddField(
            model_name="payment",
            name="doctor",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="payments", to="clinic.doctor"),
        ),
        migrations.AddField(
            model_name="payment",
            name="payer_type",
            field=models.CharField(choices=[("NORMAL", "Normal (privé)"), ("CHIFFA", "CNAS / Chiffa"), ("MIL", "Militaire")], default="NORMAL", max_length=12),
        ),
        migrations.AddField(
            model_name="payment",
            name="amount_patient",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="payment",
            name="amount_third_party",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="payment",
            name="third_party_note",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
