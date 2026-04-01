from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0005_accouchement'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicamentConsommable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=200, unique=True, verbose_name='Nom du médicament / consommable')),
                ('prix_unit', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Prix unitaire (DA)')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['nom'], 'verbose_name': 'Médicament / Consommable'},
        ),
    ]
