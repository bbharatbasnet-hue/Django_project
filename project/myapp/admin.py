from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StudentApplication, Leave, Contact


@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "last_name",
        "applying_for",
        "father_name",
        "father_contact",
        "email",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "father_name",
        "email",
    )

    list_filter = (
        "gender",
        "blood_group",
        "applying_for",
    )


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "leave_type",
        "start_date",
        "end_date",
        "status",
        "created_at",
    )

    search_fields = (
        "user__username",
        "leave_type",
    )

    list_filter = (
        "leave_type",
        "status",
    )



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "middle_name",
        "last_name",
        "date_of_birth",
        "contact_email",
        "message",
      
    )