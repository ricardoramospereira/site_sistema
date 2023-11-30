from django.shortcuts import get_object_or_404, render
from accounts.models import MyUser

# Create your views here.

def perfil_view(request, id):
    perfil = get_object_or_404(MyUser.objects.select_related('perfil'), id=id)
    context = {'obg': perfil}
    return render(request, 'user_profile/profile.html', context)