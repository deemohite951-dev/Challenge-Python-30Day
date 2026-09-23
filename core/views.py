from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import IssueReport, Category
from .forms import UserRegisterForm, IssueReportForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    issues = IssueReport.objects.select_related('category', 'reporter').all()
    total_count = issues.count()
    open_count = issues.filter(status='OPEN').count()
    in_progress_count = issues.filter(status='IN_PROGRESS').count()
    resolved_count = issues.filter(status='RESOLVED').count()

    recent_issues = issues.order_by('-created_at')[:6]

    context = {
        'total': total_count,
        'open': open_count,
        'in_progress': in_progress_count,
        'resolved': resolved_count,
        'recent_issues': recent_issues,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def feed_view(request):
    category_id = request.GET.get('category')
    status_filter = request.GET.get('status')
    
    issues = IssueReport.objects.select_related('category', 'reporter').all().order_by('-created_at')

    if category_id:
        issues = issues.filter(category_id=category_id)
    if status_filter:
        issues = issues.filter(status=status_filter)

    categories = Category.objects.all()
    return render(request, 'core/feed.html', {
        'issues': issues,
        'categories': categories,
        'selected_cat': category_id,
        'selected_status': status_filter
    })

@login_required
def report_issue_view(request):
    if request.method == 'POST':
        form = IssueReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            messages.success(request, "Issue reported successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please check the form inputs.")
    else:
        form = IssueReportForm()
    return render(request, 'core/report_wizard.html', {'form': form})