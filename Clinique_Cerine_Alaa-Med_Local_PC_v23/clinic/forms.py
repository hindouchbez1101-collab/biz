from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Patient, Appointment, Payment, PaymentItem, Expense, LabTest, LabPack, ServiceType, AppointmentStatus, Supplier, Purchase, PurchaseItem, Employee, Salary, PurchaseStatus, MedecinAmbulant

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"input", "placeholder":"Utilisateur"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"input", "placeholder":"Mot de passe"}))

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["first_name", "last_name", "phone", "birth_date", "notes"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class":"input"}),
            "last_name": forms.TextInput(attrs={"class":"input"}),
            "phone": forms.TextInput(attrs={"class":"input"}),
            "birth_date": forms.DateInput(attrs={"class":"input", "type":"date"}),
            "notes": forms.Textarea(attrs={"class":"input", "rows":3}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient", "start_at", "service_type", "status", "doctor", "note"]
        widgets = {
            "patient": forms.Select(attrs={"class":"input"}),
            "start_at": forms.DateTimeInput(attrs={"class":"input", "type":"datetime-local"}),
            "service_type": forms.Select(attrs={"class":"input"}),
            "payer_type": forms.Select(attrs={"class":"input"}),
            "doctor": forms.Select(attrs={"class":"input"}),
            "status": forms.Select(attrs={"class":"input"}),
            "doctor": forms.Select(attrs={"class":"input"}),
            "third_party_note": forms.TextInput(attrs={"class":"input"}),
            "note": forms.TextInput(attrs={"class":"input"}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["category", "amount", "spent_at", "note"]
        widgets = {
            "category": forms.Select(attrs={"class":"input"}),
            "amount": forms.NumberInput(attrs={"class":"input", "step":"0.01"}),
            "spent_at": forms.DateInput(attrs={"class":"input", "type":"date"}),
            "doctor": forms.Select(attrs={"class":"input"}),
            "third_party_note": forms.TextInput(attrs={"class":"input"}),
            "note": forms.TextInput(attrs={"class":"input"}),
        }

class PaymentForm(forms.ModelForm):
    amount_patient = forms.DecimalField(
        required=False, min_value=0, decimal_places=2, max_digits=12,
        widget=forms.NumberInput(attrs={"class": "input", "step": "0.01"}))
    amount_third_party = forms.DecimalField(
        required=False, min_value=0, decimal_places=2, max_digits=12,
        widget=forms.NumberInput(attrs={"class": "input", "step": "0.01"}))
    amount_total = forms.DecimalField(
        required=False, min_value=0, decimal_places=2, max_digits=12,
        widget=forms.NumberInput(attrs={"class": "input", "step": "0.01"}))

    def clean_amount_patient(self):
        from decimal import Decimal
        return self.cleaned_data.get('amount_patient') or Decimal('0')

    def clean_amount_third_party(self):
        from decimal import Decimal
        return self.cleaned_data.get('amount_third_party') or Decimal('0')

    def clean_amount_total(self):
        from decimal import Decimal
        return self.cleaned_data.get('amount_total') or Decimal('0')

    class Meta:
        model = Payment
        fields = ["patient", "appointment", "service_type", "payer_type", "doctor", "amount_patient", "amount_third_party", "amount_total", "third_party_note", "note"]
        widgets = {
            "patient": forms.Select(attrs={"class":"input"}),
            "appointment": forms.Select(attrs={"class":"input"}),
            "service_type": forms.Select(attrs={"class":"input"}),
            "payer_type": forms.Select(attrs={"class":"input"}),
            "doctor": forms.Select(attrs={"class":"input"}),
            "third_party_note": forms.TextInput(attrs={"class":"input"}),
            "note": forms.TextInput(attrs={"class":"input"}),
        }

class PaymentItemForm(forms.ModelForm):
    amount = forms.DecimalField(
        required=False, min_value=0, decimal_places=2, max_digits=12,
        widget=forms.NumberInput(attrs={"class": "input", "step": "0.01"}))

    class Meta:
        model = PaymentItem
        fields = ["lab_test", "label", "amount"]
        widgets = {
            "lab_test": forms.Select(attrs={"class":"input"}),
            "label": forms.TextInput(attrs={"class":"input", "placeholder":"Si pas dans la liste"}),
        }

class LabPackApplyForm(forms.Form):
    pack = forms.ModelChoiceField(queryset=LabPack.objects.filter(is_active=True), widget=forms.Select(attrs={"class":"input"}))


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "phone", "address", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class":"input"}),
            "phone": forms.TextInput(attrs={"class":"input"}),
            "address": forms.TextInput(attrs={"class":"input"}),
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["supplier", "purchased_at", "invoice_no", "status", "note"]
        widgets = {
            "supplier": forms.Select(attrs={"class":"input"}),
            "purchased_at": forms.DateInput(attrs={"class":"input", "type":"date"}),
            "invoice_no": forms.TextInput(attrs={"class":"input"}),
            "status": forms.Select(attrs={"class":"input"}),
            "note": forms.TextInput(attrs={"class":"input"}),
        }

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ["label", "qty", "unit_price"]
        widgets = {
            "label": forms.TextInput(attrs={"class":"input", "placeholder": "Code-barre ou nom article..."}),
            "qty": forms.NumberInput(attrs={"class":"input", "placeholder": "Qté", "step":"0.01"}),
            "unit_price": forms.NumberInput(attrs={"class":"input", "placeholder": "Prix achat", "step":"0.01"}),
        }
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["full_name", "role", "phone", "is_active"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class":"input"}),
            "role": forms.TextInput(attrs={"class":"input"}),
            "phone": forms.TextInput(attrs={"class":"input"}),
        }

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ["employee", "month", "amount", "paid_at", "note"]
        widgets = {
            "employee": forms.Select(attrs={"class":"input"}),
            "month": forms.DateInput(attrs={"class":"input", "type":"date"}),
            "amount": forms.NumberInput(attrs={"class":"input", "step":"0.01"}),
            "paid_at": forms.DateInput(attrs={"class":"input", "type":"date"}),
            "note": forms.TextInput(attrs={"class":"input"}),
        }


class MedecinAmbulantForm(forms.ModelForm):
    class Meta:
        model = MedecinAmbulant
        fields = ["full_name", "phone", "specialite", "is_active"]
        widgets = {
            "full_name":  forms.TextInput(attrs={"class": "input"}),
            "phone":      forms.TextInput(attrs={"class": "input"}),
            "specialite": forms.TextInput(attrs={"class": "input"}),
        }


class HonorairesPayerForm(forms.Form):
    """Marquer les honoraires d'un médecin comme payés."""
    honoraires_payes_le = forms.DateField(
        widget=forms.DateInput(attrs={"class": "input", "type": "date"}),
        label="Date de paiement",
    )


# ── Dossiers médicaux ────────────────────────────────────────────────────────
from .models import DossierMaternite, ExamenMaternite

class DossierMaterniteForm(forms.ModelForm):
    class Meta:
        model = DossierMaternite
        exclude = ['patient', 'created_by', 'created_at', 'updated_at']
        widgets = {
            'numero':           forms.TextInput(attrs={'class': 'input'}),
            'type_dossier':     forms.Select(attrs={'class': 'input'}),
            'nom':              forms.TextInput(attrs={'class': 'input'}),
            'prenom':           forms.TextInput(attrs={'class': 'input'}),
            'date_naissance':   forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'lieu_naissance':   forms.TextInput(attrs={'class': 'input'}),
            'epoux':            forms.TextInput(attrs={'class': 'input'}),
            'medecin':          forms.TextInput(attrs={'class': 'input'}),
            'service':          forms.TextInput(attrs={'class': 'input'}),
            'diagnostic':       forms.TextInput(attrs={'class': 'input'}),
            'date_entree':      forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'date_intervention':forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'date_sortie':      forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'date_depot':       forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'num_ass':          forms.TextInput(attrs={'class': 'input'}),
            'tuteur_nom':       forms.TextInput(attrs={'class': 'input'}),
            'tuteur_adresse':   forms.TextInput(attrs={'class': 'input'}),
            'tuteur_tel':       forms.TextInput(attrs={'class': 'input'}),
            'cn_pq_no':         forms.TextInput(attrs={'class': 'input'}),
            'cn_delivre_le':    forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'diagnostic_autorisation': forms.Textarea(attrs={'class': 'input', 'rows': 3}),
            'notes':            forms.Textarea(attrs={'class': 'input', 'rows': 3}),
        }


class ExamenMaterniteForm(forms.ModelForm):
    class Meta:
        model = ExamenMaternite
        exclude = ['patient', 'created_by', 'created_at', 'updated_at']
        widgets = {
            'numero_manuel':    forms.TextInput(attrs={'class': 'input'}),
            'type_examen':      forms.Select(attrs={'class': 'input'}),
            'date_examen':      forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            # Anamnèse
            'date_mariage':     forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'atcd_f':           forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'atcd_p':           forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'antecedent_med':   forms.TextInput(attrs={'class': 'input'}),
            'antecedent_chir':  forms.TextInput(attrs={'class': 'input'}),
            'antecedent_obst':  forms.TextInput(attrs={'class': 'input'}),
            'grossesse':        forms.TextInput(attrs={'class': 'input', 'style': 'width:80px'}),
            'parite':           forms.TextInput(attrs={'class': 'input', 'style': 'width:80px'}),
            'enfants_vivants':  forms.TextInput(attrs={'class': 'input', 'style': 'width:80px'}),
            'ddr':              forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'groupage':         forms.TextInput(attrs={'class': 'input'}),
            'ta':               forms.TextInput(attrs={'class': 'input'}),
            'temperature':      forms.TextInput(attrs={'class': 'input'}),
            'hu':               forms.TextInput(attrs={'class': 'input'}),
            'cu':               forms.TextInput(attrs={'class': 'input'}),
            'etat_general':     forms.TextInput(attrs={'class': 'input'}),
            'tv':               forms.TextInput(attrs={'class': 'input'}),
            'spl':              forms.TextInput(attrs={'class': 'input'}),
            'bcf':              forms.TextInput(attrs={'class': 'input'}),
            'ercf':             forms.TextInput(attrs={'class': 'input'}),
            'echo':             forms.TextInput(attrs={'class': 'input'}),
            'avis_reanima':     forms.Textarea(attrs={'class': 'input', 'rows': 2}),
            'conclusion':       forms.Textarea(attrs={'class': 'input', 'rows': 3}),
            'cat':              forms.Textarea(attrs={'class': 'input', 'rows': 3}),
            # Partogramme
            'sage_femme':       forms.TextInput(attrs={'class': 'input'}),
            'partogramme_notes':forms.Textarea(attrs={'class': 'input', 'rows': 6}),
            'prescription':     forms.Textarea(attrs={'class': 'input', 'rows': 3}),
            # Nouveau-né
            'nn_sexe':          forms.TextInput(attrs={'class': 'input'}),
            'nn_poids':         forms.TextInput(attrs={'class': 'input'}),
            'nn_apgar':         forms.TextInput(attrs={'class': 'input'}),
            'nn_notes':         forms.Textarea(attrs={'class': 'input', 'rows': 3}),
            'notes':            forms.Textarea(attrs={'class': 'input', 'rows': 2}),
        }
