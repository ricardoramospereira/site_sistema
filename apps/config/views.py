from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required
def dashboard_view(request):
    return render(request, 'config/dashboard.html')

@login_required
def config_view(request):
    return render(request, 'config/settings.html')