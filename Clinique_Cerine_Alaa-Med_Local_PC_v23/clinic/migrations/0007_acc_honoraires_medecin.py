from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0006_medicaments_salary_edit'),
    ]

    operations = [
        migrations.AddField(
            model_name='accouchementdetail',
            name='honoraires_medecin',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Honoraires médecin vacataire (DA)'),
        ),
    ]
