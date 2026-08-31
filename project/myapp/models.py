from django.db import models

# Create your models here.


class StudentApplication(models.Model):

    # ==========================================
    # 1. STUDENT INFORMATION
    # ==========================================

    first_name = models.CharField(max_length=50)

    middle_name = models.CharField(
        max_length=50,
        blank=True
    )

    last_name = models.CharField(max_length=50)

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other"),
        ]
    )

    blood_group = models.CharField(
        max_length=5,
        choices=[
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("O+", "O+"),
            ("O-", "O-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
        ]
    )

    nationality = models.CharField(
        max_length=50,
        default="Nepali"
    )

    religion = models.CharField(max_length=50)

    previous_school = models.CharField(
        max_length=150
    )


    # ==========================================
    # 2. PARENT / GUARDIAN INFORMATION
    # ==========================================

    father_name = models.CharField(
        max_length=100
    )

    mother_name = models.CharField(
        max_length=100
    )

    guardian_name = models.CharField(
        max_length=100,
        blank=True
    )

    father_contact = models.CharField(
        max_length=20
    )

    mother_contact = models.CharField(
        max_length=20
    )

    guardian_contact = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField()


    # ==========================================
    # 3. ADDRESS INFORMATION
    # ==========================================

    province = models.CharField(
        max_length=100
    )

    district = models.CharField(
        max_length=100
    )

    municipality = models.CharField(
        max_length=100
    )

    ward_no = models.CharField(
        max_length=10
    )

    tole_village = models.CharField(
        max_length=100
    )

    permanent_address = models.TextField()

    temporary_address = models.TextField()


    # ==========================================
    # 4. ACADEMIC INFORMATION
    # ==========================================

    applying_for = models.CharField(
        max_length=50
    )

    previous_class = models.CharField(
        max_length=50
    )

    previous_school_address = models.TextField()

    previous_gpa_percentage = models.CharField(
        max_length=20
    )


    # ==========================================
    # 5. ADDITIONAL INFORMATION
    # ==========================================

    student_photo = models.ImageField(
        upload_to="admission/student_photos/"
    )

    birth_certificate = models.FileField(
        upload_to="admission/birth_certificates/"
    )

    previous_school_certificate = models.FileField(
        upload_to="admission/school_certificates/"
    )

    medical_information = models.TextField(
        blank=True
    )

    emergency_contact = models.CharField(
        max_length=20
    )


    # ==========================================
    # SYSTEM INFORMATION
    # ==========================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )



from django.db import models
from django.contrib.auth.models import User


class Leave(models.Model):
    LEAVE_TYPES = [
        ("Sick Leave", "Sick Leave"),
        ("Casual Leave", "Casual Leave"),
        ("Emergency Leave", "Emergency Leave"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)




class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    contact_email = models.EmailField()
    message = models.TextField()


    def __str__(self):
        return f"{self.user.username} - {self.leave_type} ({self.status})"