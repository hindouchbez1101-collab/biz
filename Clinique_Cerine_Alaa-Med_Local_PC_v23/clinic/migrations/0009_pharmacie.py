from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0008_medecin_ambulant'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicamentPharmacie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, unique=True, verbose_name='Nom du médicament')),
                ('unite', models.CharField(blank=True, default='unité', max_length=50, verbose_name='Unité')),
                ('stock_actuel', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Stock actuel')),
                ('seuil_alerte', models.DecimalField(decimal_places=2, default=5, max_digits=10, verbose_name="Seuil d'alerte")),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Médicament pharmacie',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='MouvementPharmacie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_mouvement', models.CharField(
                    choices=[('ENTREE', 'Entrée (réception)'), ('SORTIE', 'Sortie (délivrance)')],
                    max_length=10, verbose_name='Type')),
                ('quantite', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Quantité')),
                ('destinataire', models.CharField(blank=True, default='', max_length=200, verbose_name='Délivré à / Fournisseur')),
                ('note', models.CharField(blank=True, default='', max_length=500, verbose_name='Note')),
                ('date_mouvement', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('medicament', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='mouvements',
                    to='clinic.medicamentpharmacie',
                    verbose_name='Médicament')),
                ('created_by', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='mouvements_pharmacie',
                    to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mouvement pharmacie',
                'ordering': ['-date_mouvement', '-created_at'],
            },
        ),
    ]
