from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0007_acc_honoraires_medecin'),
    ]

    operations = [
        # 1. Create MedecinAmbulant table
        migrations.CreateModel(
            name='MedecinAmbulant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, unique=True, verbose_name='Nom complet')),
                ('phone', models.CharField(blank=True, default='', max_length=60, verbose_name='Téléphone')),
                ('specialite', models.CharField(blank=True, default='', max_length=120, verbose_name='Spécialité')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Médecin ambulatoire',
                'ordering': ['full_name'],
            },
        ),
        # 2. Add FK to AccouchementDetail
        migrations.AddField(
            model_name='accouchementdetail',
            name='medecin_ambulant',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='accouchements',
                to='clinic.medecinambulant',
                verbose_name='Médecin ambulatoire',
            ),
        ),
        # 3. Add honoraires_payes boolean
        migrations.AddField(
            model_name='accouchementdetail',
            name='honoraires_payes',
            field=models.BooleanField(default=False, verbose_name='Honoraires payés'),
        ),
        # 4. Add honoraires_payes_le date
        migrations.AddField(
            model_name='accouchementdetail',
            name='honoraires_payes_le',
            field=models.DateField(blank=True, null=True, verbose_name='Payé le'),
        ),
    ]
