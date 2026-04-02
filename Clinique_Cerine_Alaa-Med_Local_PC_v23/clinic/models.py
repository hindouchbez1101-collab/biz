from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.phone})"

class Doctor(models.Model):
    full_name = models.CharField(max_length=160, unique=True)
    specialty = models.CharField(max_length=120, blank=True, default="")

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class PayerType(models.TextChoices):
    NORMAL = "NORMAL", "Normal (privé)"
    CHIFFA = "CHIFFA", "CNAS / Chiffa"
    MILITAIRE = "MIL", "Militaire"


class ServiceType(models.TextChoices):
    CONSULTATION = "CONSULT", "Consultation"
    ECHOGRAPHIE = "ECHO", "Échographie"
    ACC_NATUREL = "NAT", "Accouchement naturel"
    CESARIENNE = "CES", "Césarienne"
    ANALYSES = "LAB", "Analyses"
    AUTRE = "OTHER", "Autre"


class AppointmentStatus(models.TextChoices):
    PENDING = "PENDING", "En attente"
    CONFIRMED = "CONFIRMED", "Confirmé"
    CANCELLED = "CANCELLED", "Annulé"
    DONE = "DONE", "Terminé"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    start_at = models.DateTimeField()
    service_type = models.CharField(max_length=12, choices=ServiceType.choices)
    status = models.CharField(max_length=12, choices=AppointmentStatus.choices, default=AppointmentStatus.CONFIRMED)
    note = models.CharField(max_length=255, blank=True, default="")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_appointments")
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_at"]

    def __str__(self):
        return f"RDV {self.patient} {self.start_at:%Y-%m-%d %H:%M}"


class LabTest(models.Model):
    name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class LabPack(models.Model):
    name = models.CharField(max_length=200, unique=True)
    tests = models.ManyToManyField(LabTest, related_name="packs", blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Payment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="payments")
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name="payments")
    service_type = models.CharField(max_length=12, choices=ServiceType.choices)
    amount_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    note = models.CharField(max_length=255, blank=True, default="")
    receipt_no = models.CharField(max_length=30, unique=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_payments")
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    payer_type = models.CharField(max_length=12, choices=PayerType.choices, default=PayerType.NORMAL)
    amount_patient = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_third_party = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    third_party_note = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        ordering = ["-paid_at"]

    def __str__(self):
        return f"Reçu {self.receipt_no} - {self.patient}"


class PaymentItem(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="items")
    # for Analyses lines
    lab_test = models.ForeignKey(LabTest, on_delete=models.SET_NULL, null=True, blank=True)
    label = models.CharField(max_length=200, blank=True, default="")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def display_name(self):
        return self.lab_test.name if self.lab_test else self.label


class ExpenseCategory(models.TextChoices):
    LOYER = "LOYER", "Loyer"
    SALAIRE = "SALAIRE", "Salaire"
    MATERIEL = "MATERIEL", "Matériel"
    INTERNET = "INTERNET", "Internet"
    MAINTENANCE = "MAINTENANCE", "Maintenance"
    AUTRE = "AUTRE", "Autre"


class Expense(models.Model):
    category = models.CharField(max_length=30, choices=ExpenseCategory.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    spent_at = models.DateField()
    note = models.CharField(max_length=255, blank=True, default="")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_expenses")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-spent_at", "-created_at"]


class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True)
    phone = models.CharField(max_length=60, blank=True, default="")
    address = models.CharField(max_length=255, blank=True, default="")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PurchaseStatus(models.TextChoices):
    DRAFT = "DRAFT", "Brouillon"
    PENDING = "PENDING", "En attente validation"
    APPROVED = "APPROVED", "Validé"
    RECEIVED = "RECEIVED", "Réceptionné"
    PAID = "PAID", "Payé"
    CANCELLED = "CANCELLED", "Annulé"


class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="purchases")
    invoice_no = models.CharField(max_length=60, blank=True, default="")
    purchased_at = models.DateField()
    status = models.CharField(max_length=12, choices=PurchaseStatus.choices, default=PurchaseStatus.PENDING)
    note = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_purchases")
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_purchases")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["-purchased_at", "-created_at"]

    def __str__(self):
        return f"{self.supplier} - {self.purchased_at}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
    label = models.CharField(max_length=200)
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.line_total = (self.qty or 0) * (self.unit_price or 0)
        super().save(*args, **kwargs)


class Employee(models.Model):
    full_name = models.CharField(max_length=200, unique=True)
    role = models.CharField(max_length=120, blank=True, default="")
    phone = models.CharField(max_length=60, blank=True, default="")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="salaries")
    month = models.DateField(help_text="Utiliser le 1er jour du mois (ex: 2026-02-01)")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateField(null=True, blank=True)
    note = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_salaries")

    class Meta:
        ordering = ["-month", "employee__full_name"]
        unique_together = [("employee", "month")]

    def __str__(self):
        return f"{self.employee} - {self.month}"


class AuditLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=80)
    entity = models.CharField(max_length=80)
    entity_id = models.CharField(max_length=40, blank=True, default="")
    message = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


# ═══════════════════════════════════════════════════════════════════════════════
#  DOSSIERS MÉDICAUX MATERNITÉ
# ═══════════════════════════════════════════════════════════════════════════════

class TypeDossier(models.TextChoices):
    GENERAL   = "GENERAL",   "Maternité (Général)"
    CHIFA     = "CHIFA",     "Maternité Chifa ACC"
    MILITAIRE = "MILITAIRE", "Maternité Militaire"


class DossierMaternite(models.Model):
    patient           = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="dossiers")
    numero            = models.CharField(max_length=40, unique=True, verbose_name="N° Dossier")
    type_dossier      = models.CharField(max_length=12, choices=TypeDossier.choices, default=TypeDossier.GENERAL, verbose_name="Type")

    # Identité
    nom               = models.CharField(max_length=120)
    prenom            = models.CharField(max_length=120)
    date_naissance    = models.DateField(null=True, blank=True)
    lieu_naissance    = models.CharField(max_length=200, blank=True, default="")
    epoux             = models.CharField(max_length=200, blank=True, default="", verbose_name="Époux")

    # Prise en charge
    medecin           = models.CharField(max_length=160, blank=True, default="", verbose_name="Médecin")
    service           = models.CharField(max_length=120, blank=True, default="")
    diagnostic        = models.CharField(max_length=255, blank=True, default="")
    date_entree       = models.DateField(null=True, blank=True, verbose_name="Date d'entrée")
    date_intervention = models.DateField(null=True, blank=True, verbose_name="Date d'intervention")
    date_sortie       = models.DateField(null=True, blank=True, verbose_name="Date de sortie")
    date_depot        = models.DateField(null=True, blank=True, verbose_name="Date dépôt dossier")
    num_ass           = models.CharField(max_length=80, blank=True, default="", verbose_name="N° Ass / N° Militaire")

    # Autorisation d'opérer
    tuteur_nom        = models.CharField(max_length=200, blank=True, default="", verbose_name="Père / Tuteur / Mari")
    tuteur_adresse    = models.CharField(max_length=255, blank=True, default="", verbose_name="Adresse tuteur")
    tuteur_tel        = models.CharField(max_length=40, blank=True, default="", verbose_name="Tél tuteur")
    cn_pq_no          = models.CharField(max_length=80, blank=True, default="", verbose_name="CN/PQ N°")
    cn_delivre_le     = models.DateField(null=True, blank=True, verbose_name="Délivré le")
    diagnostic_autorisation = models.TextField(blank=True, default="", verbose_name="Diagnostic (autorisation)")

    notes             = models.TextField(blank=True, default="")
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)
    created_by        = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_dossiers")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Dossier {self.numero} — {self.nom} {self.prenom} [{self.get_type_dossier_display()}]"


# ═══════════════════════════════════════════════════════════════════════════════
#  EXAMENS MATERNITÉ (ANAMNÈSE / PARTOGRAMME / NOUVEAU-NÉ)
# ═══════════════════════════════════════════════════════════════════════════════

class TypeExamen(models.TextChoices):
    ANAMNESE    = "ANAMNESE",    "Anamnèse"
    PARTOGRAMME = "PARTOGRAMME", "Partogramme (Surveillance du travail)"
    NOUVEAU_NE  = "NOUVEAU_NE",  "Examen nouveau-né"


class ExamenMaternite(models.Model):
    patient          = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="examens")
    numero_manuel    = models.CharField(max_length=40, unique=True, verbose_name="N° Examen (manuel)")
    type_examen      = models.CharField(max_length=16, choices=TypeExamen.choices, default=TypeExamen.ANAMNESE, verbose_name="Type d'examen")
    date_examen      = models.DateField(verbose_name="Date de l'examen")

    # ── Anamnèse ─────────────────────────────────────────────────────────────
    date_mariage     = models.DateField(null=True, blank=True, verbose_name="Date de mariage")
    atcd_f           = models.TextField(blank=True, default="", verbose_name="ATCD Familiaux (AT CD F)")
    atcd_p           = models.TextField(blank=True, default="", verbose_name="ATCD Personnels (AT CD P)")
    antecedent_med   = models.TextField(blank=True, default="", verbose_name="Antécédents Médecine")
    antecedent_chir  = models.TextField(blank=True, default="", verbose_name="Antécédents Chirurgicaux")
    antecedent_obst  = models.TextField(blank=True, default="", verbose_name="Antécédents Obstétricaux")
    grossesse        = models.CharField(max_length=10, blank=True, default="", verbose_name="G (Grossesses)")
    parite           = models.CharField(max_length=10, blank=True, default="", verbose_name="P (Parité)")
    enfants_vivants  = models.CharField(max_length=10, blank=True, default="", verbose_name="Enfants vivants")
    # Examen clinique
    ddr              = models.DateField(null=True, blank=True, verbose_name="DDR")
    groupage         = models.CharField(max_length=10, blank=True, default="", verbose_name="Groupage")
    ta               = models.CharField(max_length=20, blank=True, default="", verbose_name="TA")
    temperature      = models.CharField(max_length=10, blank=True, default="", verbose_name="T°")
    hu               = models.CharField(max_length=20, blank=True, default="", verbose_name="HU")
    cu               = models.CharField(max_length=20, blank=True, default="", verbose_name="CU")
    etat_general     = models.CharField(max_length=80, blank=True, default="", verbose_name="État général")
    tv               = models.CharField(max_length=100, blank=True, default="", verbose_name="TV")
    spl              = models.CharField(max_length=80, blank=True, default="", verbose_name="SPL")
    bcf              = models.CharField(max_length=40, blank=True, default="", verbose_name="BCF")
    ercf             = models.CharField(max_length=80, blank=True, default="", verbose_name="ERCF")
    echo             = models.CharField(max_length=200, blank=True, default="", verbose_name="ECHO")
    avis_reanima     = models.TextField(blank=True, default="", verbose_name="Avis réanimation-anesthésie")
    conclusion       = models.TextField(blank=True, default="", verbose_name="Conclusion")
    cat              = models.TextField(blank=True, default="", verbose_name="CAT")

    # ── Partogramme ──────────────────────────────────────────────────────────
    sage_femme       = models.CharField(max_length=160, blank=True, default="", verbose_name="Sage-femme / Médecin")
    partogramme_notes = models.TextField(blank=True, default="", verbose_name="Données partogramme")
    prescription     = models.TextField(blank=True, default="", verbose_name="Prescription")

    # ── Nouveau-né ────────────────────────────────────────────────────────────
    nn_sexe          = models.CharField(max_length=10, blank=True, default="", verbose_name="Sexe")
    nn_poids         = models.CharField(max_length=20, blank=True, default="", verbose_name="Poids (g)")
    nn_apgar         = models.CharField(max_length=40, blank=True, default="", verbose_name="Score Apgar")
    nn_notes         = models.TextField(blank=True, default="", verbose_name="Notes nouveau-né")

    notes            = models.TextField(blank=True, default="", verbose_name="Notes complémentaires")
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    created_by       = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_examens")

    class Meta:
        ordering = ["-date_examen", "-created_at"]

    def __str__(self):
        return f"Examen {self.numero_manuel} — {self.get_type_examen_display()} — {self.patient}"


# ═══════════════════════════════════════════════════════════════════════════════
#  TARIFS ACCOUCHEMENT — Configurables dans les Paramètres
# ═══════════════════════════════════════════════════════════════════════════════

class TarifAccouchement(models.Model):
    """Tarifs par défaut pour les frais d'accouchement. Un seul enregistrement (singleton)."""
    salle               = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Salle d'accouchement / Bloc opératoire (DA)")
    sejour_nuit         = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Séjour par nuit (DA)")
    anesthesie          = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Frais anesthésie (DA)")
    sage_femme          = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Frais sage-femme (DA)")
    frais_admin         = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Frais administratifs / dossier (DA)")
    certificat_naissance= models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Certificat de naissance (DA)")
    frais_chifa         = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Frais dossier Chifa / Militaire (DA)")
    medicaments_defaut  = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Médicaments & consommables (DA — défaut)")
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tarif accouchement"

    def __str__(self):
        return "Tarifs accouchement"

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ═══════════════════════════════════════════════════════════════════════════════
#  DÉTAIL FRAIS ACCOUCHEMENT — Lié à un encaissement
# ═══════════════════════════════════════════════════════════════════════════════

class AccouchementDetail(models.Model):
    payment             = models.OneToOneField('Payment', on_delete=models.CASCADE, related_name='acc_detail')
    type_acte           = models.CharField(max_length=10, choices=[('NAT','Accouchement naturel'),('CES','Césarienne')], default='NAT')

    # Frais de base
    salle               = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Salle / Bloc")
    nb_nuits            = models.PositiveIntegerField(default=1, verbose_name="Nombre de nuits")
    tarif_nuit          = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Tarif / nuit")
    anesthesie          = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Anesthésie")
    sage_femme          = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Sage-femme")
    medicaments         = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Médicaments & consommables")
    frais_admin         = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Frais administratifs")
    certificat_naissance= models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Certificat de naissance")
    frais_chifa         = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Frais dossier Chifa/Militaire")

    # Honoraires médecin vacataire (ex: médecin extérieur appelé pour l'accouchement)
    honoraires_medecin  = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Honoraires médecin vacataire (DA)")

    # Notes libres
    notes               = models.TextField(blank=True, default='', verbose_name="Notes complémentaires")

    created_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Détail accouchement"

    def sejour_total(self):
        return (self.nb_nuits or 0) * float(self.tarif_nuit or 0)

    def total_frais(self):
        return (
            float(self.salle or 0) +
            self.sejour_total() +
            float(self.anesthesie or 0) +
            float(self.sage_femme or 0) +
            float(self.medicaments or 0) +
            float(self.frais_admin or 0) +
            float(self.certificat_naissance or 0) +
            float(self.frais_chifa or 0) +
            float(self.honoraires_medecin or 0)
        )

    def __str__(self):
        return f"Détail acc. — {self.payment}"


# ═══════════════════════════════════════════════════════════════════════════════
#  MÉDICAMENTS & CONSOMMABLES
# ═══════════════════════════════════════════════════════════════════════════════

class MedicamentConsommable(models.Model):
    nom       = models.CharField(max_length=200, unique=True, verbose_name="Nom du médicament / consommable")
    prix_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Prix unitaire (DA)")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["nom"]
        verbose_name = "Médicament / Consommable"

    def __str__(self):
        return self.nom
