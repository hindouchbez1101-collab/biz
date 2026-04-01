from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0004_dossiers_medicaux'),
    ]

    operations = [
        migrations.CreateModel(
            name='TarifAccouchement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('salle', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="Salle d'accouchement / Bloc opératoire (DA)")),
                ('sejour_nuit', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Séjour par nuit (DA)')),
                ('anesthesie', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Frais anesthésie (DA)')),
                ('sage_femme', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Frais sage-femme (DA)')),
                ('frais_admin', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Frais administratifs / dossier (DA)')),
                ('certificat_naissance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Certificat de naissance (DA)')),
                ('frais_chifa', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Frais dossier Chifa / Militaire (DA)')),
                ('medicaments_defaut', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Médicaments & consommables (DA — défaut)')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': 'Tarif accouchement'},
        ),
        migrations.CreateModel(
            name='AccouchementDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('payment', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='acc_detail',
                    to='clinic.payment',
                )),
                ('type_acte', models.CharField(
                    choices=[('NAT', 'Accouchement naturel'), ('CES', 'Césarienne')],
                    default='NAT', max_length=10,
                )),
                ('salle', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Salle / Bloc')),
                ('nb_nuits', models.PositiveIntegerField(default=1, verbose_name='Nombre de nuits')),
                ('tarif_nuit', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Tarif / nuit')),
                ('anesthesie', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Anesthésie')),
                ('sage_femme', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Sage-femme')),
                ('medicaments', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Médicaments & consommables')),
                ('frais_admin', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Frais administratifs')),
                ('certificat_naissance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Certificat de naissance')),
                ('frais_chifa', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Frais dossier Chifa/Militaire')),
                ('notes', models.TextField(blank=True, default='', verbose_name='Notes complémentaires')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Détail accouchement'},
        ),
    ]
