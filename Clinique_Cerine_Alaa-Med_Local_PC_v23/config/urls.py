from django.contrib import admin
from django.urls import path
from clinic import views as v

urlpatterns = [
    path("admin/", admin.site.urls),

    path("login/", v.login_view, name="login"),
    path("logout/", v.logout_view, name="logout"),

    path("", v.home, name="home"),

    # Réception
    path("patients/", v.patient_list, name="patient_list"),
    path("patients/new/", v.patient_new, name="patient_new"),
    path("patients/<int:pk>/", v.patient_detail, name="patient_detail"),

    path("rdv/", v.appointment_list, name="appointment_list"),
    path("rdv/new/", v.appointment_new, name="appointment_new"),
    path("rdv/<int:pk>/edit/", v.appointment_edit, name="appointment_edit"),

    path("encaissements/", v.payment_list, name="payment_list"),
    path("encaissements/new/", v.payment_new, name="payment_new"),
    path("encaissements/<int:pk>/recu/", v.payment_receipt, name="payment_receipt"),

    # Finance
    path("depenses/", v.expense_list, name="expense_list"),
    path("depenses/new/", v.expense_new, name="expense_new"),
    path("depenses/<int:pk>/edit/", v.expense_edit, name="expense_edit"),
    path("finance/caisse/", v.caisse_solde, name="caisse_solde"),
    path("depenses/excel/", v.expense_export_excel, name="expense_export_excel"),
    path("depenses/pdf/", v.expense_export_pdf, name="expense_export_pdf"),

    path("rapports/", v.reports, name="reports"),
    path("rapports/excel/", v.reports_export_excel, name="reports_export_excel"),
    path("rapports/pdf/", v.reports_export_pdf, name="reports_export_pdf"),

    # Stock & Logistique
    path("stock/fournisseurs/", v.suppliers_list, name="suppliers_list"),
    path("stock/fournisseurs/new/", v.supplier_new, name="supplier_new"),
    path("stock/fournisseurs/<int:pk>/edit/", v.supplier_edit, name="supplier_edit"),

    path("stock/achats/", v.purchases_list, name="purchases_list"),
    path("stock/achats/new/", v.purchase_new, name="purchase_new"),
    path("stock/achats/<int:pk>/edit/", v.purchase_edit, name="purchase_edit"),
    path("stock/achats/<int:pk>/bl/", v.purchase_delivery_note, name="purchase_delivery_note"),
    path("stock/achats/item/<int:pk>/del/", v.purchase_delete_item, name="purchase_delete_item"),

    # RH
    path("rh/salaires/", v.salaries_dashboard, name="salaries_dashboard"),
    path("rh/salaires/new/", v.salary_new, name="salary_new"),
    path("rh/employes/", v.employees_list, name="employees_list"),
    path("rh/employes/new/", v.employee_new, name="employee_new"),
    path("rh/salaires/<int:pk>/edit/", v.salary_edit, name="salary_edit"),
    path("rh/employes/<int:pk>/edit/", v.employee_edit, name="employee_edit"),

    # Admin (in-app)
    path("parametres/", v.settings_view, name="settings_view"),

    # Dossiers médicaux maternité
    path("dossiers/",                                  v.dossier_list,   name="dossier_list"),
    path("dossiers/patients/<int:patient_pk>/new/",    v.dossier_new,    name="dossier_new"),
    path("dossiers/<int:pk>/",                         v.dossier_detail, name="dossier_detail"),
    path("dossiers/<int:pk>/edit/",                    v.dossier_edit,   name="dossier_edit"),

    # Examens maternité (anamnèse / partogramme / nouveau-né)
    path("examens/",                                   v.examen_list,    name="examen_list"),
    path("examens/patients/<int:patient_pk>/new/",     v.examen_new,     name="examen_new"),
    path("examens/<int:pk>/",                          v.examen_detail,  name="examen_detail"),
    path("examens/<int:pk>/edit/",                     v.examen_edit,    name="examen_edit"),

    # Sortie & complétion dossier
    path("dossiers/<int:pk>/sortie/",                   v.dossier_sortie,  name="dossier_sortie"),
    path("examens/<int:pk>/completer/",                  v.examen_completer, name="examen_completer"),

    # Caisse intelligente — génération automatique depuis dossier
    path("encaissements/caisse/",                       v.caisse_view,    name="caisse_view"),
    path("encaissements/api/patient-dossier/",          v.api_patient_dossier, name="api_patient_dossier"),

    # Médecins ambulatoires
    path("medecins-ambulants/",                         v.medecin_ambulant_list,   name="medecin_ambulant_list"),
    path("medecins-ambulants/new/",                     v.medecin_ambulant_new,    name="medecin_ambulant_new"),
    path("medecins-ambulants/<int:pk>/",                v.medecin_ambulant_detail, name="medecin_ambulant_detail"),
    path("medecins-ambulants/<int:pk>/edit/",           v.medecin_ambulant_edit,   name="medecin_ambulant_edit"),
    path("medecins-ambulants/honoraires/<int:acc_pk>/payer/",   v.honoraires_mark_paid,   name="honoraires_mark_paid"),
    path("medecins-ambulants/honoraires/<int:acc_pk>/annuler/", v.honoraires_mark_unpaid, name="honoraires_mark_unpaid"),
]
