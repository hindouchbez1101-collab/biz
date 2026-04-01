from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0003_stock_hr'),
    ]

    operations = [
        # ── Dossier Maternité ────────────────────────────────────────────────
        migrations.CreateModel(
            name='DossierMaternite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=40, unique=True, verbose_name='N° Dossier')),
                ('type_dossier', models.CharField(
                    max_length=12,
                    choices=[
                        ('GENERAL',    'Maternité (Général)'),
                        ('CHIFA',      'Maternité Chifa ACC'),
                        ('MILITAIRE',  'Maternité Militaire'),
                    ],
                    default='GENERAL',
                    verbose_name='Type de dossier',
                )),
                # Identité
                ('nom',               models.CharField(max_length=120)),
                ('prenom',            models.CharField(max_length=120)),
                ('date_naissance',    models.DateField(null=True, blank=True)),
                ('lieu_naissance',    models.CharField(max_length=200, blank=True, default='')),
                ('epoux',             models.CharField(max_length=200, blank=True, default='', verbose_name='Époux')),
                # Prise en charge
                ('medecin',           models.CharField(max_length=160, blank=True, default='', verbose_name='Médecin')),
                ('service',           models.CharField(max_length=120, blank=True, default='')),
                ('diagnostic',        models.CharField(max_length=255, blank=True, default='')),
                ('date_entree',       models.DateField(null=True, blank=True, verbose_name="Date d'entrée")),
                ('date_intervention', models.DateField(null=True, blank=True, verbose_name="Date d'intervention")),
                ('date_sortie',       models.DateField(null=True, blank=True, verbose_name='Date de sortie')),
                ('date_depot',        models.DateField(null=True, blank=True, verbose_name='Date dépôt dossier')),
                ('num_ass',           models.CharField(max_length=80, blank=True, default='', verbose_name='N° Ass / N° Militaire')),
                # Autorisation d'opérer
                ('tuteur_nom',        models.CharField(max_length=200, blank=True, default='', verbose_name='Père / Tuteur / Mari')),
                ('tuteur_adresse',    models.CharField(max_length=255, blank=True, default='', verbose_name='Adresse tuteur')),
                ('tuteur_tel',        models.CharField(max_length=40, blank=True, default='', verbose_name='Tél tuteur')),
                ('cn_pq_no',          models.CharField(max_length=80, blank=True, default='', verbose_name='CN/PQ N°')),
                ('cn_delivre_le',     models.DateField(null=True, blank=True, verbose_name='Délivré le')),
                ('diagnostic_autorisation', models.TextField(blank=True, default='', verbose_name='Diagnostic (autorisation)')),
                # Notes libres
                ('notes',             models.TextField(blank=True, default='')),
                # Méta
                ('created_at',        models.DateTimeField(auto_now_add=True)),
                ('updated_at',        models.DateTimeField(auto_now=True)),
                ('patient',           models.ForeignKey(
                    'clinic.Patient',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='dossiers',
                )),
                ('created_by',        models.ForeignKey(
                    'auth.User',
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='created_dossiers',
                )),
            ],
            options={'ordering': ['-created_at']},
        ),

        # ── Examen Maternité (Anamnèse) ──────────────────────────────────────
        migrations.CreateModel(
            name='ExamenMaternite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_manuel',     models.CharField(max_length=40, unique=True, verbose_name='N° Examen (manuel)')),
                ('type_examen',       models.CharField(
                    max_length=16,
                    choices=[
                        ('ANAMNESE',    'Anamnèse'),
                        ('PARTOGRAMME', 'Partogramme (Surveillance du travail)'),
                        ('NOUVEAU_NE',  'Examen nouveau-né'),
                    ],
                    default='ANAMNESE',
                    verbose_name="Type d'examen",
                )),
                ('date_examen',       models.DateField(verbose_name="Date de l'examen")),
                # ── Anamnèse ──────────────────────────────────────────────────
                ('date_mariage',      models.DateField(null=True, blank=True, verbose_name='Date de mariage')),
                ('atcd_f',            models.TextField(blank=True, default='', verbose_name='ATCD Familiaux (AT CD F)')),
                ('atcd_p',            models.TextField(blank=True, default='', verbose_name='ATCD Personnels (AT CD P)')),
                ('antecedent_med',    models.TextField(blank=True, default='', verbose_name='Antécédents Médecine')),
                ('antecedent_chir',   models.TextField(blank=True, default='', verbose_name='Antécédents Chirurgicaux')),
                ('antecedent_obst',   models.TextField(blank=True, default='', verbose_name='Antécédents Obstétricaux')),
                ('grossesse',         models.CharField(max_length=10, blank=True, default='', verbose_name='G (Grossesses)')),
                ('parite',            models.CharField(max_length=10, blank=True, default='', verbose_name='P (Parité)')),
                ('enfants_vivants',   models.CharField(max_length=10, blank=True, default='', verbose_name='Enfants vivants')),
                # Examen clinique
                ('ddr',               models.DateField(null=True, blank=True, verbose_name='DDR')),
                ('groupage',          models.CharField(max_length=10, blank=True, default='', verbose_name='Groupage')),
                ('ta',                models.CharField(max_length=20, blank=True, default='', verbose_name='TA')),
                ('temperature',       models.CharField(max_length=10, blank=True, default='', verbose_name='T°')),
                ('hu',                models.CharField(max_length=20, blank=True, default='', verbose_name='HU')),
                ('cu',                models.CharField(max_length=20, blank=True, default='', verbose_name='CU')),
                ('etat_general',      models.CharField(max_length=80, blank=True, default='', verbose_name='État général')),
                ('tv',                models.CharField(max_length=100, blank=True, default='', verbose_name='TV')),
                ('spl',               models.CharField(max_length=80, blank=True, default='', verbose_name='SPL')),
                ('bcf',               models.CharField(max_length=40, blank=True, default='', verbose_name='BCF')),
                ('ercf',              models.CharField(max_length=80, blank=True, default='', verbose_name='ERCF')),
                ('echo',              models.CharField(max_length=200, blank=True, default='', verbose_name='ECHO')),
                ('avis_reanima',      models.TextField(blank=True, default='', verbose_name='Avis réanimation-anesthésie')),
                ('conclusion',        models.TextField(blank=True, default='', verbose_name='Conclusion')),
                ('cat',               models.TextField(blank=True, default='', verbose_name='CAT')),
                # ── Partogramme ───────────────────────────────────────────────
                ('sage_femme',        models.CharField(max_length=160, blank=True, default='', verbose_name='Sage-femme / Médecin')),
                ('partogramme_notes', models.TextField(blank=True, default='', verbose_name='Données partogramme (lignes)')),
                ('prescription',      models.TextField(blank=True, default='', verbose_name='Prescription')),
                # ── Nouveau-né ────────────────────────────────────────────────
                ('nn_sexe',           models.CharField(max_length=10, blank=True, default='', verbose_name='Sexe')),
                ('nn_poids',          models.CharField(max_length=20, blank=True, default='', verbose_name='Poids (g)')),
                ('nn_apgar',          models.CharField(max_length=40, blank=True, default='', verbose_name='Score Apgar')),
                ('nn_notes',          models.TextField(blank=True, default='', verbose_name='Notes nouveau-né')),
                # Méta
                ('notes',             models.TextField(blank=True, default='', verbose_name='Notes complémentaires')),
                ('created_at',        models.DateTimeField(auto_now_add=True)),
                ('updated_at',        models.DateTimeField(auto_now=True)),
                ('patient',           models.ForeignKey(
                    'clinic.Patient',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='examens',
                )),
                ('created_by',        models.ForeignKey(
                    'auth.User',
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='created_examens',
                )),
            ],
            options={'ordering': ['-date_examen', '-created_at']},
        ),
    ]
