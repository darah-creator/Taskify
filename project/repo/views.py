from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tasks
from .forms import TaskForm, SubmissionForm
from django.contrib.auth.models import User

def staff_check(user):
    return user.is_staff


# ---------------- USER ---------------- #

@login_required
def submit_task(request, pk):
    """User submits work for a task assigned to them."""
    task = get_object_or_404(Tasks, pk=pk, assigned_to=request.user)

    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.status = "submitted"
            task.save()
            return redirect("dashboard:user_dashboard")
    else:
        form = SubmissionForm(instance=task)

    return render(request, "submit_task.html", {"task": task, "form": form})

def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()

            if form.cleaned_data["assign_all"]:
                # Assign to all users
                task.assigned_to.set(User.objects.all())
            else:
                # Assign only selected users
                task.assigned_to.set(form.cleaned_data["assign_to"])

            return redirect("dashboard:admin_dashboard")  # Adjust to your route
    else:
        form = TaskForm()

    return render(request, "create_task.html", {"form": form})


@user_passes_test(staff_check, login_url="signin")
def review_task(request, pk):
    """Admin reviews and grades a submitted task."""
    task = get_object_or_404(Tasks, pk=pk)

    if request.method == "POST":
        status = request.POST.get("status")

        if status == "graded":
            try:
                task.grade = int(request.POST.get("grade", 0))
            except ValueError:
                task.grade = 0
            task.status = "graded"

        elif status == "rejected":
            task.status = "rejected"

        task.save()
        return redirect("dashboard:admin_dashboard")

    return render(request, "review_task.html", {"task": task})



@login_required
def delete_task(request, pk):
    task = get_object_or_404(Tasks, pk=pk, assigned_to=request.user)


    # Only allow deletion if still submitted and not graded yet
    if task.status == "submitted":
        task.file.delete()  # assuming Task has a related Submission
        task.status = "assigned"
        task.save()

    return redirect("dashboard:user_dashboard")