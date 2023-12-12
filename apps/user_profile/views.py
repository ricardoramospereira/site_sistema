from django.shortcuts import get_object_or_404, render
from accounts.models import MyUser
from django.contrib.auth.decorators import login_required

# Só é permitido ver o perfil para quem está logado
@login_required()
def perfil_view(request, username):
    filtro = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum') # restagata todos os objetos relacionados com myuser em lote

    perfil = get_object_or_404(filtro, username=username)
    context = {'obj': perfil}
    return render(request, 'user_profile/profile.html', context)