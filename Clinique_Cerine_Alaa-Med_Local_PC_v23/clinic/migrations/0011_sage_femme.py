from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0010_acte_chirurgical'),
    ]

    operations = [
        migrations.CreateModel(
            name='SageFemme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, unique=True, verbose_name='Nom complet')),
                ('phone', models.CharField(blank=True, default='', max_length=60, verbose_name='Téléphone')),
                ('specialite', models.CharField(blank=True, default='', max_length=120, verbose_name='Spécialité / Service')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Sage-femme',
                'ordering': ['full_name'],
            },
        ),
        migrations.AddField(
            model_name='accouchementdetail',
            name='sage_femme_ext',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='accouchements',
                to='clinic.sagefemme',
                verbose_name='Sage-femme ambulatoire',
            ),
        ),
        migrations.AddField(
            model_name='accouchementdetail',
            name='honoraires_sf_payes',
            field=models.BooleanField(default=False, verbose_name='Honoraires SF payés'),
        ),
        migrations.AddField(
            model_name='accouchementdetail',
            name='honoraires_sf_payes_le',
            field=models.DateField(blank=True, null=True, verbose_name='SF payée le'),
        ),
        # Rename verbose_name on existing fields (data-only, no schema change needed)
    ]
