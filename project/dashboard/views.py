from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from repo.models import Tasks


def staff_check(user):
    return user.is_authenticated and user.is_staff


@login_required
def dashboard_home(request):
    """
    Entry point:
    - Staff → admin dashboard
    - Normal user → user dashboard
    """
    if request.user.is_staff:
        return redirect("dashboard:admin_dashboard")
    return redirect("dashboard:user_dashboard")


# ---------------- USER DASHBOARD ---------------- #
@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return redirect("dashboard:admin_dashboard")

    user_tasks = Tasks.objects.filter(assigned_to=request.user).order_by("-created_at")

    context = {
        "user": request.user,
        "tasks": user_tasks,
        "total": user_tasks.count(),
        "graded": user_tasks.filter(status="graded").count(),
        "pending": user_tasks.filter(status="pending").count(),
        "rejected": user_tasks.filter(status="rejected").count(),
    }
    return render(request, "dashboard/user_dashboard.html", context)


# ---------------- ADMIN DASHBOARD ---------------- #
@user_passes_test(staff_check, login_url="signin")
def admin_dashboard(request):
    """
    Dashboard for staff/admin users.
    Shows overview + tasks waiting for grading.
    """
    total_tasks = Tasks.objects.count()

    ungraded_tasks = Tasks.objects.filter(status="submitted").order_by("-created_at")
    graded_tasks = Tasks.objects.filter(status="graded")  # 👈 add this

    context = {
        "user": request.user,
        "total_tasks": total_tasks,
        "ungraded_count": ungraded_tasks.count(),
        "ungraded_tasks": ungraded_tasks[:10],  # show 10 recent ungraded
        "graded_tasks": graded_tasks,
        "recent_tasks": Tasks.objects.order_by("-created_at")[:10],
    }
    return render(request, "dashboard/admin_dashboard.html", context)
