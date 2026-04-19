from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0009_pharmacie'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActeChirurgicalDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prix_acte', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="PRX de l'acte")),
                ('nuite_nb', models.PositiveIntegerField(default=0, verbose_name='Nombre de nuités')),
                ('nuite_prix', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Prix / nuit')),
                ('garde_nb', models.PositiveIntegerField(default=0, verbose_name='Nombre gardes')),
                ('garde_prix', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Prix / garde')),
                ('bilan_desc', models.CharField(blank=True, default='', max_length=300, verbose_name='Bilan ajouté (description)')),
                ('bilan_total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Bilan total')),
                ('traitement_desc', models.CharField(blank=True, default='', max_length=300, verbose_name='Traitement associé (description)')),
                ('traitement_total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Traitement total')),
                ('oxygene_total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Oxygène bébé total')),
                ('transfusion_total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Transfusion total')),
                ('notes', models.TextField(blank=True, default='', verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='acte_detail',
                    to='clinic.payment',
                )),
            ],
            options={
                'verbose_name': 'Détail acte chirurgical',
            },
        ),
    ]
