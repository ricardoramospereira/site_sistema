from django.shortcuts import get_object_or_404, render
from accounts.models import MyUser
from django.contrib.auth.decorators import login_required

# Só é permitido ver o perfil para quem está logado
@login_required()
def perfil_view(request, username):
    perfil = get_object_or_404(MyUser.objects.select_related('perfil'), username=username)
    context = {'obj': perfil}
    return render(request, 'user_profile/profile.html', context)