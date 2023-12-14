from django.shortcuts import get_object_or_404, render
from accounts.models import MyUser
from django.contrib.auth.decorators import login_required

from posts.forms import PostagemForumForm

# Só é permitido ver o perfil para quem está logado
@login_required()
def perfil_view(request, username):
    filtro = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum') # resgata todos os objetos relacionados com myuser em lote
    perfil = get_object_or_404(filtro, username=username)

    form_dict = {}
    for el in perfil.user_postagem_forum.all():
        form = PostagemForumForm(instance=el)
        form_dict[el] = form

    context = {'obj': perfil, 'form_dict': form_dict}

    return render(request, 'user_profile/profile.html', context)
