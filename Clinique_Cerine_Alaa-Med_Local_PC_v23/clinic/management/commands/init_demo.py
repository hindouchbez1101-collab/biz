from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.db import transaction
from clinic.models import LabTest, LabPack, Doctor, Supplier, Employee

GROUPS = ["RECEPTION", "GERANT", "ADMIN"]

DEFAULT_ANALYSES = [
    "NFS (Numération Formule Sanguine)",
    "Hémoglobine (Hb)",
    "Hématocrite (Ht)",
    "Plaquettes",
    "Globules blancs (GB)",
    "Groupe sanguin ABO + Rh",
    "RAI (Recherche d’Agglutinines Irrégulières)",
    "VS (Vitesse de sédimentation)",
    "TP / INR",
    "TCA",
    "Glycémie à jeun",
    "Glycémie post-prandiale",
    "HbA1c",
    "Urée",
    "Créatinine",
    "Acide urique",
    "Cholestérol total",
    "HDL",
    "LDL",
    "Triglycérides",
    "ASAT (TGO)",
    "ALAT (TGP)",
    "GGT",
    "Phosphatases alcalines (PAL)",
    "Bilirubine totale",
    "Bilirubine directe",
    "Protéines totales",
    "Albumine",
    "CRP",
    "Ionogramme (Na, K, Cl)",
    "Calcium",
    "Magnésium",
    "Fer sérique",
    "Ferritine",
    "TSH",
    "FT4",
    "FT3",
    "Prolactine",
    "FSH",
    "LH",
    "Estradiol (E2)",
    "Progestérone",
    "Testostérone",
    "β-hCG (dosage sanguin)",
    "Toxoplasmose IgG/IgM",
    "Rubéole IgG/IgM",
    "CMV IgG/IgM",
    "HBsAg (Hépatite B)",
    "HCV (Hépatite C)",
    "HIV 1&2",
    "Syphilis (VDRL/TPHA)",
    "ECBU",
    "Bandelette urinaire",
    "Protéinurie 24h",
    "Test de grossesse urinaire",
]

DEFAULT_SUPPLIERS = [
    ("Pharma Central", "0550 00 00 00"),
    ("Matériel Médical Pro", "0770 00 00 00"),
]
DEFAULT_EMPLOYEES = [
    ("Moussa", "Réception"),
    ("Samira", "Infirmière"),
]

DEFAULT_DOCTORS = [
    ("Dr. A. Gynéco", "Gynécologie"),
    ("Dr. B. Généraliste", "Médecine générale"),
]

PACKS = {
    "Pack Grossesse – 1er trimestre": [
        "NFS (Numération Formule Sanguine)",
        "Groupe sanguin ABO + Rh",
        "RAI (Recherche d’Agglutinines Irrégulières)",
        "Glycémie à jeun",
        "Toxoplasmose IgG/IgM",
        "Rubéole IgG/IgM",
        "HIV 1&2",
        "HBsAg (Hépatite B)",
        "Syphilis (VDRL/TPHA)",
        "ECBU",
    ],
    "Pack Suivi grossesse (contrôle)": [
        "NFS (Numération Formule Sanguine)",
        "Glycémie à jeun",
        "Urée",
        "Créatinine",
        "Protéinurie 24h",
        "Bandelette urinaire",
    ],
    "Pack Diabète": [
        "Glycémie à jeun",
        "HbA1c",
        "Glycémie post-prandiale",
        "Urée",
        "Créatinine",
    ],
    "Pack Thyroïde": [
        "TSH",
        "FT4",
        "FT3",
    ],
    "Pack Bilan hormonal femme": [
        "FSH",
        "LH",
        "Prolactine",
        "Estradiol (E2)",
        "Progestérone",
    ],
    "Pack Bilan général": [
        "NFS (Numération Formule Sanguine)",
        "Glycémie à jeun",
        "Urée",
        "Créatinine",
        "Cholestérol total",
        "Triglycérides",
        "ASAT (TGO)",
        "ALAT (TGP)",
    ],
}

class Command(BaseCommand):
    help = "Initialise groupes/roles + admin demo + liste analyses + packs."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Groups
        for g in GROUPS:
            Group.objects.get_or_create(name=g)

        # Users
        if not User.objects.filter(username="admin").exists():
            u = User.objects.create_superuser("admin", password="admin12345")
            self.stdout.write(self.style.WARNING("Utilisateur admin créé: admin / admin12345"))
        else:
            u = User.objects.get(username="admin")

        # Create demo reception and gerant
        if not User.objects.filter(username="reception").exists():
            r = User.objects.create_user("reception", password="recep12345")
            r.groups.add(Group.objects.get(name="RECEPTION"))
            self.stdout.write(self.style.WARNING("Utilisateur reception créé: reception / recep12345"))
        if not User.objects.filter(username="gerant").exists():
            g = User.objects.create_user("gerant", password="gerant12345")
            g.groups.add(Group.objects.get(name="GERANT"))
            self.stdout.write(self.style.WARNING("Utilisateur gerant créé: gerant / gerant12345"))

        # Ensure admin group
        u.groups.add(Group.objects.get(name="ADMIN"))

        # Suppliers
        for name, phone in DEFAULT_SUPPLIERS:
            Supplier.objects.get_or_create(name=name, defaults={"phone": phone})

        # Employees
        for full_name, role in DEFAULT_EMPLOYEES:
            Employee.objects.get_or_create(full_name=full_name, defaults={"role": role})

        # Doctors
        for full_name, specialty in DEFAULT_DOCTORS:
            Doctor.objects.get_or_create(full_name=full_name, defaults={"specialty": specialty})

        # Lab tests
        existing = set(LabTest.objects.values_list("name", flat=True))
        for name in DEFAULT_ANALYSES:
            if name not in existing:
                LabTest.objects.create(name=name, is_active=True)

        # Packs
        for pack_name, test_names in PACKS.items():
            pack, _ = LabPack.objects.get_or_create(name=pack_name, defaults={"is_active": True})
            tests = list(LabTest.objects.filter(name__in=test_names))
            pack.tests.set(tests)
            pack.is_active = True
            pack.save()

        self.stdout.write(self.style.SUCCESS("Initialisation terminée."))
