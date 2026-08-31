from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .form import LeaveForm
from .models import Leave
from .models import Contact

# STATIC / INFO PAGES

def home(request):
    return render(request, 'main/home.html')


def contact(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name")
        last_name = request.POST.get("last_name")
        date_of_birth = request.POST.get("date_of_birth")
        contact_email = request.POST.get("contact_email")
        message = request.POST.get("message")

        Contact.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            contact_email=contact_email,
            message=message
        )

        return redirect("contact")

    return render(request, 'main/contact.html')


def about(request):
    return render(request, 'main/about.html')


def form(request):
    return render(request, 'main/form.html')



# AUTHENTICATION


def _add_bootstrap_classes(form):
    """Add Bootstrap's form-control class to every field widget."""
    for field in form.fields.values():
        field.widget.attrs.update({"class": "form-control"})


def register(request):

    if request.user.is_authenticated:
        return redirect("leave_list")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        _add_bootstrap_classes(form)

        if form.is_valid():
            user = form.save()

            # Send welcome email
            send_mail(
                subject="Welcome to the Leave Management System",
                message=f"""Hello {user.username},

Your account has been created successfully.
You can now log in and apply for leave.

Thank you.
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email] if user.email else [],
                fail_silently=True,
            )

            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
        _add_bootstrap_classes(form)

    return render(request, "registration/register.html", {"form": form})


# LEAVE — CRUD


def _send_leave_email(user, subject, leave, extra_note=""):
    """Small helper so every leave action sends a consistent email."""
    send_mail(
        subject=subject,
        message=f"""Hello {user.username},

{extra_note}

Leave Type: {leave.leave_type}
Start Date: {leave.start_date}
End Date: {leave.end_date}
Reason: {leave.reason}
Status: {leave.status}

Thank you.
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email] if user.email else [],
        fail_silently=True,
    )


@login_required
def apply_leave(request):
    """CREATE"""

    if request.method == "POST":
        form = LeaveForm(request.POST)

        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()

            _send_leave_email(
                request.user,
                "Leave Application Submitted",
                leave,
                "Your leave application has been submitted successfully.",
            )

            messages.success(request, "Leave application submitted successfully!")
            return redirect("leave_list")

    else:
        form = LeaveForm()

    return render(request, "main/apply_leave.html", {"form": form})


@login_required
def leave_list(request):
    """READ (list) — only the logged-in user's own leaves"""

    leaves = Leave.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "main/leave_list.html", {"leaves": leaves})


@login_required
def leave_detail(request, pk):
    """READ (single)"""

    leave = get_object_or_404(Leave, pk=pk, user=request.user)

    return render(request, "main/leave_detail.html", {"leave": leave})


@login_required
def leave_edit(request, pk):
    """UPDATE — only allowed while status is still Pending"""

    leave = get_object_or_404(Leave, pk=pk, user=request.user)

    if leave.status != "Pending":
        messages.error(request, "Only pending leave requests can be edited.")
        return redirect("leave_detail", pk=leave.pk)

    if request.method == "POST":
        form = LeaveForm(request.POST, instance=leave)

        if form.is_valid():
            leave = form.save()

            _send_leave_email(
                request.user,
                "Leave Application Updated",
                leave,
                "Your leave application has been updated successfully.",
            )

            messages.success(request, "Leave application updated successfully!")
            return redirect("leave_detail", pk=leave.pk)
    else:
        form = LeaveForm(instance=leave)

    return render(request, "main/leave_edit.html", {"form": form, "leave": leave})


@login_required
def leave_delete(request, pk):
    """DELETE — only allowed while status is still Pending"""

    leave = get_object_or_404(Leave, pk=pk, user=request.user)

    if request.method == "POST":
        if leave.status != "Pending":
            messages.error(request, "Only pending leave requests can be deleted.")
            return redirect("leave_detail", pk=leave.pk)

        # Capture details before deletion for the email
        leave_type, start_date, end_date = leave.leave_type, leave.start_date, leave.end_date
        user = request.user
        leave.delete()

        send_mail(
            subject="Leave Application Deleted",
            message=f"""Hello {user.username},

Your leave application has been deleted.

Leave Type: {leave_type}
Start Date: {start_date}
End Date: {end_date}

Thank you.
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email] if user.email else [],
            fail_silently=True,
        )

        messages.success(request, "Leave application deleted successfully!")
        return redirect("leave_list")

    return render(request, "main/leave_confirm_delete.html", {"leave": leave})
