from django.contrib import admin
from .models import Doctor, PayerType, Patient, Appointment, Payment, PaymentItem, Expense, LabTest, LabPack, AuditLog, Supplier, Purchase, PurchaseItem, Employee, Salary, PurchaseStatus

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name", "phone"]
    list_display = ["last_name", "first_name", "phone", "created_at"]

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["start_at", "patient", "service_type", "status", "doctor", "created_by"]
    list_filter = ["service_type", "status"]
    search_fields = ["patient__first_name", "patient__last_name", "patient__phone"]

class PaymentItemInline(admin.TabularInline):
    model = PaymentItem
    extra = 0

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["paid_at", "receipt_no", "patient", "service_type", "payer_type", "amount_total", "amount_patient", "amount_third_party", "doctor", "created_by"]
    list_filter = ["service_type"]
    search_fields = ["receipt_no", "patient__phone", "patient__first_name", "patient__last_name"]
    inlines = [PaymentItemInline]

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["spent_at", "category", "amount", "created_by"]
    list_filter = ["category"]
    search_fields = ["note"]

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]

@admin.register(LabPack)
class LabPackAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]
    filter_horizontal = ["tests"]

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["created_at", "actor", "action", "entity", "entity_id"]
    search_fields = ["action", "entity", "entity_id", "message", "actor__username"]

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ["full_name", "specialty"]
    search_fields = ["full_name", "specialty"]


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "is_active"]
    search_fields = ["name", "phone"]
    list_filter = ["is_active"]

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["purchased_at", "supplier", "status", "total_amount", "invoice_no", "created_by", "approved_by"]
    list_filter = ["status", "purchased_at", "supplier"]
    search_fields = ["supplier__name", "invoice_no", "note"]
    inlines = [PurchaseItemInline]

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["full_name", "role", "phone", "is_active"]
    search_fields = ["full_name", "role", "phone"]
    list_filter = ["is_active"]

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ["month", "employee", "amount", "paid_at", "created_by"]
    list_filter = ["month", "paid_at"]
    search_fields = ["employee__full_name", "note"]
