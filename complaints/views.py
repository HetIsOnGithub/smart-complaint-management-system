from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, ComplaintForm, RegisterForm
from .gemini import generate_complaint_details
from .models import Comment, Complaint


def is_admin(user):
    return user.is_staff or user.is_superuser


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration completed successfully.")
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
        },
    )


@login_required
def dashboard(request):
    complaints = Complaint.objects.filter(user=request.user)

    context = {
        "complaints": complaints,
        "total_complaints": complaints.count(),
        "pending_count": complaints.filter(status="Pending").count(),
        "in_progress_count": complaints.filter(status="In Progress").count(),
        "resolved_count": complaints.filter(status="Resolved").count(),
    }

    return render(
        request,
        "dashboard.html",
        context,
    )

@login_required
def submit_complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)

        if form.is_valid():
            complaint = form.save(commit=False)

            ai_data = generate_complaint_details(
                complaint.description
            )

            complaint.user = request.user
            complaint.title = ai_data["title"]
            complaint.category = ai_data["category"]
            complaint.priority = ai_data["priority"]
            complaint.status = "Pending"

            complaint.save()

            messages.success(
                request,
                "Complaint submitted successfully.",
            )

            return redirect(
                "complaint_detail",
                pk=complaint.pk,
            )
    else:
        form = ComplaintForm()

    return render(
        request,
        "complaint_form.html",
        {
            "form": form,
        },
    )
    
@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(
        Complaint,
        pk=pk,
    )

    if not request.user.is_staff and complaint.user != request.user:
        messages.error(
            request,
            "You are not authorized to view this complaint.",
        )
        return redirect("dashboard")

    comments = complaint.comments.select_related("user").all()

    context = {
        "complaint": complaint,
        "comments": comments,
        "comment_form": CommentForm(),
    }

    return render(
        request,
        "complaint_detail.html",
        context,
    )


@login_required
def add_comment(request, pk):
    complaint = get_object_or_404(
        Complaint,
        pk=pk,
    )

    if not request.user.is_staff and complaint.user != request.user:
        messages.error(
            request,
            "You are not authorized to comment on this complaint.",
        )
        return redirect("dashboard")

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.complaint = complaint
            comment.user = request.user
            comment.save()

            messages.success(
                request,
                "Comment added successfully.",
            )

        else:
            messages.error(
                request,
                "Please enter a valid comment.",
            )

    return redirect(
        "complaint_detail",
        pk=complaint.pk,
    )

@login_required   
@user_passes_test(is_admin)
def admin_dashboard(request):
    complaints = (
        Complaint.objects
        .select_related("user")
        .prefetch_related("comments")
        .order_by("-created_at")
    )

    context = {
        "complaints": complaints,
        "total_complaints": complaints.count(),
        "pending_count": complaints.filter(status="Pending").count(),
        "in_progress_count": complaints.filter(status="In Progress").count(),
        "resolved_count": complaints.filter(status="Resolved").count(),
        "total_users": User.objects.count(),
        "total_comments": Comment.objects.count(),
    }

    return render(
        request,
        "admin_dashboard.html",
        context,
    )

@login_required
@user_passes_test(is_admin)
def update_status(request, pk):
    complaint = get_object_or_404(
        Complaint,
        pk=pk,
    )

    if request.method == "POST":
        status = request.POST.get("status")

        valid_status = {
            "Pending",
            "In Progress",
            "Resolved",
        }

        if status in valid_status:
            complaint.status = status
            complaint.save(update_fields=["status", "updated_at"])

            messages.success(
                request,
                "Complaint status updated successfully.",
            )
        else:
            messages.error(
                request,
                "Invalid complaint status.",
            )

    return redirect("admin_dashboard")

@login_required
@user_passes_test(is_admin)
def delete_complaint(request, pk):
    complaint = get_object_or_404(
        Complaint,
        pk=pk,
    )

    if request.method == "POST":
        complaint.delete()

        messages.success(
            request,
            "Complaint deleted successfully.",
        )

    return redirect("admin_dashboard")

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("admin_dashboard")
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)

            messages.success(
                request,
                "Login successful."
            )

            if user.is_staff:
                return redirect("admin_dashboard")

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "registration/login.html",
    )
    
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    messages.success(
        request,
        "You have been logged out successfully."
    )
    return redirect("home")