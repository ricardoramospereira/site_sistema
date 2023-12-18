from django.shortcuts import get_object_or_404, render
from accounts.models import MyUser
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

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
    # Criar uma lista de tuplas (postagem, form) a partir do form_dict
    form_list = [(postagem, form) for postagem, form in form_dict.items()]
    # Aplicar a paginação à lista de tuplas
    paginacao = Paginator(form_list, 3)
    # Obter o número da página a partir dos parâmetros da URL
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    # Criar um novo dicionário form_dict com base na página atual
    form_dict = {postagem: form for postagem, form in page_obj}
    context = {'obj': perfil, 'page_obj': page_obj, 'form_dict':form_dict}
    return render(request, 'user_profile/profile.html', context)
